#!/bin/bash
###############################################################################
# PURPOSE: Automate the build process for IPFire packages (.ipfire).
#          Uses a staging area to map the new repository structure.
#          Logic: Stage -> Generate Backup -> Generate Manifest -> Pack.
#
# HISTORY:
# 2026-03-17 | v1.2.0 | Hybrid Build Logic for Jon Murphy's structure.
###############################################################################

# 1. Initialize variables first
DEBUG="${DEBUG:-false}"
NAME="rpz"
VERSION="${1:-0.1.20.21}"
AUTHOR="H&M"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="${REPO_ROOT}/build"
MANIFEST="${REPO_ROOT}/ROOTFILES"
REPO_NAME=$(basename "${REPO_ROOT}")
PACKAGE_NAME="${REPO_NAME}-v${VERSION}.ipfire"
PAYLOAD_NAME="files.tar.xz"

# 2. Define functions

setup_staging_area() {
    # Pseudocode: Initial staging of static files from Jon Murphy's structure
    # 1. Clear and recreate a temporary staging directory.
    # 2. Map CGI scripts, sbin binaries, and language files to system paths.
    # 3. Export the path for other functions to use as the simulated root.
    local staging="${REPO_ROOT}/src_staging"
    rm -rf "$staging" && mkdir -p "$staging"

    # Map static assets
    mkdir -p "$staging/srv/web/ipfire/cgi-bin"
    cp -r "${REPO_ROOT}/html/cgi-bin/." "$staging/srv/web/ipfire/cgi-bin/"
    mkdir -p "$staging/usr/sbin"
    cp -p "${REPO_ROOT}/config/rpz/"rpz-* "$staging/usr/sbin/" 2>/dev/null
    mkdir -p "$staging/var/ipfire/addon-lang"
    cp -p "${REPO_ROOT}/config/rpz/"*.pl "$staging/var/ipfire/addon-lang/"

    mkdir -p "$staging/var/ipfire/backup/addons/includes"
    # Ensure the backup includes directory exists for the next step
    cp -pr "${REPO_ROOT}/config/backup/includes/." "$staging/var/ipfire/backup/addons/includes/" 2>/dev/null

    # FIX: Map persistent data structures so generate_backup_includes can find them
    mkdir -p "$staging/etc/unbound/zonefiles"
    mkdir -p "$staging/var/ipfire/dns/rpz"

    # Map Data Structure (Required by rpz-make)
    mkdir -p "$staging/etc/unbound/zonefiles"
    touch "$staging/etc/unbound/zonefiles/allow.rpz"
    touch "$staging/etc/unbound/zonefiles/block.rpz"
    mkdir -p "$staging/var/ipfire/dns/rpz"
    touch "$staging/var/ipfire/dns/rpz/allowlist"
    touch "$staging/var/ipfire/dns/rpz/blocklist"

    # Map WebGUI Menu entries for the package
    mkdir -p "$staging/var/ipfire/menu.d"
    cp -p "${REPO_ROOT}/config/menu/EX-rpz.menu" "$staging/var/ipfire/menu.d/" 2>/dev/null

    # Copy the *.rpz files so those get in the backup includes and manifest
    cp -p "${REPO_ROOT}/config/rpz/zonefiles/"*.rpz "$staging/etc/unbound/zonefiles/" 2>/dev/null

    # FIX: Map Unbound Integration Config 
    # module-config: "respip validator iterator" | zonefile: /etc/unbound/zonefiles/allow.rpz | rpz-action-override: passthru
    mkdir -p "$staging/etc/unbound/local.d"
    cp -p "${REPO_ROOT}/config/rpz/00-rpz.conf" "$staging/etc/unbound/local.d/" 2>/dev/null

    export FINAL_SRC="$staging"
}

generate_rootfiles() {
    # Pseudocode: use FINAL_SRC staging to generate the final ROOTFILES manifest
    # 1. Create the ROOTFILES header.
    # 2. Run find against the staging area to capture all files and directories, including backup metadata.
    # 3. Sort and strip staging prefixes for the final manifest.
    printf "# %s manifest\n# Generated: %s\n\n" "$NAME" "$(date)" > "$MANIFEST"
    
    # This command now captures var/ipfire/backup/addons/includes/rpz - files and folders included!
    # FIX: Exclude the top-level staging directories themselves from the manifest (these are Linux folders!), but include their contents
    find "$FINAL_SRC" -mindepth 1 | sed "s|${FINAL_SRC}/||" | sort | \
    # FIX: exclude Linux system folders or IPFIre native folders - those do not belong to manifest, but we want to keep the leaf nodes we created for RPZ data structure and backup includes
    grep -vE '^(etc|usr|var|srv|srv/web|srv/web/ipfire|etc/unbound|var/ipfire|var/ipfire/backup|var/ipfire/backup/addons|var/ipfire/backup/addons/includes)$' | \
    while read -r line; do
        # Check each line if it is a directory with subdirectories or files inside
        if [ -d "$FINAL_SRC/$line" ]; then
            # Keep leaf nodes we created for RPZ data structure, but exclude the top-level staging directories themselves
            [[ "$line" =~ ^(etc/unbound/zonefiles|var/ipfire/dns/rpz)$ ]] && echo "$line"
        else
            # Files - we keep those
            echo "$line"
        fi
    done >> "$MANIFEST"
}

purge_ghost_files() {
    # Pseudocode: Remove user-specific config files so they aren't packed in tar
    [ "${DEBUG}" = true ] && printf "[DEBUG] Purging ghost files from staging...\n"
    rm -f "$FINAL_SRC/etc/unbound/zonefiles/"*.rpz
    rm -f "$FINAL_SRC/var/ipfire/dns/rpz/"*
}

sanitize_build_perms() {
    # Pseudocode: 
    # 1. Apply global read permissions to all staged files/folders.
    # 2. Grant 755 (executable) permissions to CGI scripts and system binaries.
    
    [ "${DEBUG}" = true ] && printf "[DEBUG] Sanitizing staging permissions...\n"
    find "$FINAL_SRC" -type d -exec chmod 755 {} +
    find "$FINAL_SRC" -type f -exec chmod 644 {} +
    
    # Restore execution bits for specific paths
    [ -d "$FINAL_SRC/srv/web/ipfire/cgi-bin" ] && chmod 755 "$FINAL_SRC/srv/web/ipfire/cgi-bin/"*
    [ -d "$FINAL_SRC/usr/sbin" ] && chmod 755 "$FINAL_SRC/usr/sbin/"*
}

build_package() {
    # Pseudocode: 
    # 1. Compress the staged files into a .tar.xz payload using numeric-owner.
    # 2. Wrap the payload, manifest, and control scripts into the final .ipfire archive.
    # 3. Store the final package in the designated builds/ folder.
    # 4. Clean up the staging area and temporary payload.
    
    [ ! -d "$BUILD_DIR" ] && mkdir -p "$BUILD_DIR"
    
    # Create the internal payload
    cd "$FINAL_SRC" || exit 1
    # Standard IPFire: No leading dot-slash in archive, and ShellCheck safe.
    tar --numeric-owner -cJf "${BUILD_DIR}/${PAYLOAD_NAME}" -C "$FINAL_SRC" -- *
    
    # Assemble the .ipfire package using control scripts from Jon's source
    cd "${REPO_ROOT}" || exit 1
    local ctrl_src="${REPO_ROOT}/src/paks/rpz"
    tar -cvf "${BUILD_DIR}/${PACKAGE_NAME}" \
        -C "$ctrl_src" install.sh update.sh uninstall.sh \
        -C "${REPO_ROOT}" ROOTFILES \
        -C "${BUILD_DIR}" "${PAYLOAD_NAME}"
    
    # Final cleanup
    rm -f "${BUILD_DIR}/${PAYLOAD_NAME}"
    rm -rf "$FINAL_SRC"
    #rm -f "$MANIFEST"
}

generate_checksum() {
    # Pseudocode: Calculate the SHA256 hash of the generated .ipfire file for integrity verification.
    cd "${BUILD_DIR}" || exit 1
    sha256sum "${PACKAGE_NAME}" > "${PACKAGE_NAME}.sha256"
}

check_rootfiles() {
    # Pseudocode: 
    # 1. Check if ROOTFILES exists.
    # 2. Check if ROOTFILES is not empty.
    # 3. Verify each listed path exists physically.
    
    [ "${DEBUG}" = true ] && printf "[DEBUG] [%s v%s] Starting integrity checks...\n" "${AUTHOR}" "${VERSION}"

    # Edge Case 1: ROOTFILES missing
    if [ ! -f "${MANIFEST}" ]; then
        printf "ERROR: Manifest file %s not found in current directory.\n" "${MANIFEST}"
        exit 1
    fi

    # Edge Case 2: ROOTFILES is empty
    if [ ! -s "${MANIFEST}" ]; then
        printf "ERROR: Manifest file %s is empty. Build aborted.\n" "${MANIFEST}"
        exit 1
    fi

    # Edge Case 3: Verify content vs physical files
    while IFS= read -r line || [ -n "${line}" ]; do
        [[ "${line}" =~ ^#.* ]] && continue # Skip comments
        [[ -z "${line}" ]] && continue      # Skip empty lines
        
        if [ ! -e "${FINAL_SRC}/${line}" ]; then
            printf "ERROR: File listed in %s DOES NOT EXIST: %s\n" "${MANIFEST}" "${line}"
            exit 1
        fi
    done < "${MANIFEST}"
}

# 3. Execution logic
setup_staging_area         # 1. Create the system tree in staging - including backup file
generate_rootfiles         # 2. Generate ROOTFILES (with backup/includes file!)
check_rootfiles            # 3. Verify ROOTFILES integrity before packing
purge_ghost_files          # 4. Remove user-specific config files from staging
sanitize_build_perms       # 5. Fix permissions
build_package              # 6. Archive
generate_checksum          # 7. Security Hash

printf "Build Success: %s/%s | Author: %s\n" "build" "${PACKAGE_NAME}" "${AUTHOR}"

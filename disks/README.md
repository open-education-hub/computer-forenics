# Disk and Filesystem Forensics Challenges

This document provides exercises on disk and filesystem forensics. The challenges cover four major filesystems (FAT, NTFS, EXT4, and APFS).
They are mostly designed to be solved on a Linux system using command-line tools, primarily [The Sleuth Kit (TSK)](https://www.sleuthkit.org/), but any other disk forensic tools could be used.

## Area 1: FAT32 Forensics

### Very Basic: List Files

You are given `fat32.img`. List all the files in its root directory.

**Assets:**
- `fat32.img`

**Hints:**
- The Sleuth Kit's `fls` command lists files in a disk image.

### Basic: View a Deleted File

A file named `secret.txt` was deleted from the `fat32.img` disk image. Find this deleted file and view its contents.

**Assets:**
- `fat32.img`

**Hints:**
- `fls` can show deleted files. Look for entries marked with an asterisk (`*`).
- The `icat` command can extract a file's content using its inode number.

### Intermediate: Recover a Deleted File

You have identified the deleted file `secret.txt` and its inode. Now, recover the file and save it to your local disk as `recovered_secret.txt`.

**Assets:**
- `fat32.img`

**Hints:**
- `icat` can redirect its output to a file.

### Advanced: Find File Fragments with `blkls`

A large file was deleted. Even if its metadata is gone, its data blocks might still be on the disk. Examine the unallocated blocks in the image to find any readable data.

**Assets:**
- `fat32_adv.img`

**Hints:**
- The `blkls` command can show the content of unallocated blocks.

## Area 2: NTFS Forensics

### Very Basic: List Files in the MFT

You are given `ntfs.img`. List all files by examining the Master File Table (MFT).

**Assets:**
- `ntfs.img`

**Hints:**
- `fls` works on NTFS images too.

### Basic: View an Alternate Data Stream (ADS)

The file `file.txt` seems normal, but it has a secret hidden in an Alternate Data Stream. Find and read the content of the hidden stream.

**Assets:**
- An `ntfs_ads.img` with a file containing an ADS named `hidden_stream`.

**Hints:**
- `fls` will show ADS if they exist.
- `icat` can read from an ADS using the syntax `inode:stream_name`.

### Intermediate: Analyze a Resident File

Small files on NTFS can be "resident," meaning their data is stored inside the MFT record itself, not in external clusters. Find the MFT record for `small.txt` and confirm its data is resident.

**Assets:**
- `ntfs.img`

**Hints:**
- The `istat` command provides detailed metadata about a file from its MFT entry.
- Look for the term "resident" in the `istat` output.

### Advanced: Carve a Deleted File from the MFT

The resident file `small.txt` was deleted. Because its data was in the MFT, it may still be there even if the file is marked as deleted. Directly examine the MFT to find the data.

**Assets:**
- `ntfs.img` with the deleted `small.txt`.

**Hints:**
- The MFT is itself a file, the first file in the filesystem (inode 0).
- You can use `icat` to dump the MFT and then `strings` to search it.

## Area 3: EXT4 Forensics

### Very Basic: View Filesystem Metadata

You are given `ext4.img`. Display its superblock information, which contains core metadata about the filesystem.

**Assets:**
- `ext4.img`

**Hints:**
- The `fsstat` command displays filesystem-level details.

### Basic: Find a Deleted File in the Journal

A file was recently deleted from `ext4.img`. Its contents might still be in the filesystem's journal. Find the content of the deleted file.

**Assets:**
- `ext4.img`

**Hints:**
- The journal is like a log of recent filesystem changes.
- The `jls` command can list the contents of the journal. `jcat` can display it.

## Area 4: APFS Forensics

### Very Basic: View Filesystem Metadata

Examine the provided APFS image. Your task is to list all files and extract any additional metadata such as tags or comments associated with them.

Hint: APFS stores extended metadata in special attributes.

### Basic: List Snapshots

Analyze the APFS container structure, identifying all volumes. Locate any snapshots and determine what changes occurred between snapshots.

Hint: APFS containers can hold multiple volumes. Look for snapshot metadata in volume structures.

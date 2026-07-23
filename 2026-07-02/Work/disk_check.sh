#!/bin/zsh
echo
echo -e "\033[31mChecking Disk Health\033[0m"
echo
echo -e "\033[32mUsed Space in Disk\033[0m"
echo
df -h
echo
echo -e "\033[32mDisk Information\033[0m"
echo
diskutil list
echo
echo -e "\033[32mDisk Status\033[0m"
echo
diskutil info /
echo

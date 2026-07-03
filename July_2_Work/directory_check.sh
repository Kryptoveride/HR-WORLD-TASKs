#!/bin/zsh
echo
echo -e "\033[31mPlease Enter the name of the Directoy\033[0m"
read INPUT
echo
RESULT=$(find / -type d -name "$INPUT" 2>/dev/null)

if [ -n "$RESULT" ]; then
    echo -e "\033[32mDirectory found:\033[0m"
    echo "$RESULT"
else
    echo -e "\033[31mDirectory not found\033[0m."
fi
echo

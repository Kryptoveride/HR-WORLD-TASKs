#!/bin/zsh
echo
echo "Identify the number of times sudo was used"
echo
COUNT=$(grep -c "sudo" ~/.zsh_history)
echo
echo "Total number of times sudo commands used :$COUNT"
echo
echo "Last 5 sudo commands:"
grep "sudo" ~/.zsh_history | tail -5
echo

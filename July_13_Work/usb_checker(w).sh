#!/bin/zsh

echo "=============================="
echo "Active System Hardware"
echo "=============================="

system_profiler SPHardwareDataType |
grep -E "Model Name|Model Identifier|Chip|Processor Name|Processor Speed|Total Number of Cores|Memory"

echo
echo "=============================="
echo "Connected USB Storage"
echo "=============================="

usb_devices=$(diskutil list external physical 2>/dev/null | awk '/^\/dev\/disk/ {print $1}')

if [[ -z "$usb_devices" ]]; then
    echo "No external storage devices connected."
    exit 0
fi

found_usb=false

while IFS= read -r device; do
    protocol=$(diskutil info "$device" | awk -F: '/Protocol/ {
        gsub(/^[ \t]+/, "", $2)
        print $2
        exit
    }')

    if [[ "$protocol" == "USB" ]]; then
        found_usb=true

        name=$(diskutil info "$device" | awk -F: '/Device \/ Media Name/ {
            gsub(/^[ \t]+/, "", $2)
            print $2
            exit
        }')

        size=$(diskutil info "$device" | awk -F: '/Disk Size/ {
            gsub(/^[ \t]+/, "", $2)
            print $2
            exit
        }')

        echo "Device Name: ${name:-Unknown}"
        echo "Device Path: $device"
        echo "Disk Size:   ${size:-Unknown}"
        echo "Protocol:    $protocol"
        echo "------------------------------"
    fi
done <<< "$usb_devices"

if [[ "$found_usb" == false ]]; then
    echo "No USB storage devices connected."
fi
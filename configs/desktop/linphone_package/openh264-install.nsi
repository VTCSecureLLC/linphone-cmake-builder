SectionGetFlags ${msopenh264} $0
IntOp $0 $0 & ${SF_SELECTED}
IntCmpU $0 0 done done download
download:
NSISdl::download http://ciscobinary.openh264.org/openh264-1.5.0-win32msvc.dll.bz2 $INSTDIR\lib\mediastreamer\plugins\openh264.dll.bz2
ExecWait '"$INSTDIR\bin\bunzip2.exe" "$INSTDIR\lib\mediastreamer\plugins\openh264.dll.bz2"'
done:
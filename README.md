# FileSec 
##### _Secure File System_

## How to use
- open Terminal / cmd prompt and run ```python main.py <<file_Path>>``` 
    -  __Followed by Option__
      - ```-h``` for help
      - ```-e``` for file encryption
      - ```-d``` for decryption
      - ```-f``` for forgot password (while decrypting)
      - ```-r``` for added password to external device
      - ```-o``` for opening the file automatically after decryption 
- Examples
  - __*Music.mp3*__ needs to be encrypted
    - ```python main.py music.mp3 -e```
  - Decrpting the same encrypted file
    - ```python main.py music.lck -d```
  - In case of Forgot password
    - ```python main.py music.lck -d -f```
  - Storing and calling external device for saved passwords
    - ```python main.py music.mp3 -e -r ext_device_path``` while saving password
    - ```python main.py music.mp3 -d -r ext_device_path``` without typing password  
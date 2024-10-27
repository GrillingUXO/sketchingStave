# sketcingStave
基于musicxml的音符成像艺术

不同记谱软件的默认排版可能无法按预期渲染乐谱，此处给出的是适于museScore的.mss格式文件。其他记谱软件的格式文件（.lib和.musx）等待补充。大体思路无非就是staffDistance调整为16sp，noteDistance调整为0sp，一行固定为10个小节，一页容纳80个小节，手动调整即可。：
<img width="1280" alt="Screen Shot 2024-10-26 at 1 16 50 PM" src="https://github.com/user-attachments/assets/28159cb5-0d21-4322-8ab6-d52b611c7842">
<img width="1280" alt="Screen Shot 2024-10-26 at 1 17 10 PM" src="https://github.com/user-attachments/assets/b90bc1ec-32a5-448b-b863-9e9b66742c00">
<img width="1280" alt="Screen Shot 2024-10-26 at 1 17 43 PM" src="https://github.com/user-attachments/assets/26d57227-07f0-42ae-938b-1f6c86719b43">
<img width="1280" alt="Screen Shot 2024-10-26 at 1 18 05 PM" src="https://github.com/user-attachments/assets/20ed755d-c6da-4a43-abbf-e4ae2bb4a014">

原图：
<img width="471" alt="Screen Shot 2024-10-26 at 11 41 24 AM" src="https://github.com/user-attachments/assets/6c70e5cd-ce90-4e62-9f89-30def3bfdc2e">



请确保你已安装 Python 3.x，安装后请通过以下命令安装环境依赖：
```bash
pip3 install -r requirements.txt

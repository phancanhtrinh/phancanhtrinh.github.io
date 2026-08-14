---
layout: post
title: 'Hiện file ẩn do virus trong USB'
date: 2015-03-14T07:47:00.002000+07:00
categories:
  - diary
permalink: /diary/2015/03/14/hi-n-file-n-do-virus-trong-usb/
source_url: https://phancanhtrinh.blogspot.com/2015/03/hien-file-do-virus-trong-usb.html
---
<div style="text-align: justify;">
<span style="color: #444444;">Virus là một trong những phiền toái lớn của người dùng máy tính; những nỗi khốn đốn này thường đi kèm với anh bạn không thể không nhắc tới là chiếc USB. Lỗi thường gặp nhất là các file trong USB bị sau khi nhiễm virus, nhiều người tá hỏa lên với vấn đề này vì tưởng rằng dữ liệu của họ đã bị gặm nhấm hết. Thật ra các dữ liệu này vẫn còn ở đó chỉ là bị ẩn đi thôi. Đặc điểm các virus này thường khóa luôn chức năng hiện file trong </span><b><span style="color: #38761d;">Folder Option</span></b><span style="color: #444444;"> nên khó lòng lấy lại được dễ dàng. Những trường hợp cấp bách như vậy chúng ta có thể áp dụng một số cách sau:</span></div>
<div style="text-align: justify;">
<b><span style="color: orange;">Cách 1. Thử hiện file trong Folder Option</span></b></div>
<div style="text-align: justify;">
<span style="color: #444444;">Đặt các thuộc tính như hình bên dưới, lưu ý mục </span><b><span style="color: #38761d;">Hide protected operating system files... </span></b><span style="color: #444444;">không được chọn. Cuối cùng nhấn OK và xem kết quả.</span></div>
<div class="separator" style="clear: both; text-align: center;">
<img border="0" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgADy2Iw6PGMrnYFBXEaxfKbqHYyABjMzXLG4N7HbZx4kZ-iju_cmeDjCyBG1bSxE_WHA8126ZuP69jzIaB4bY5s9ZwuaBmoSJlfJ7ZTjsz-Zghm6BY-sf1-5yHfd7x0fm8U8sctapUtDI/s1600/13-03-2015+10-28-46+CH.jpg" width="305" /><img border="0" height="400" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5oVfDNaLQNIyYPgXDNc6-oDuyQHdMlqV7BGdSW_UilZJ-crPIJdmauidrYqfpSuV1PEhhbAW0_kUa0Qwl0NOzivB-HVtLY9_Z-pVRcl5YxCPGG3jKpocwgM_VbNB7U5ncPFxw8fv3wo0/s1600/13-03-2015+10-32-37+CH.jpg" width="328" /></div>
<div class="separator" style="clear: both; text-align: left;">
<b><span style="color: orange;"></span></b></div>
<a name='more'></a><b><span style="color: orange;">Cách 2. Gõ lệnh hiện file vào cmd</span></b><br />
<div class="separator" style="clear: both; text-align: left;">
<span style="color: #444444;">Bấm Window + R để mở lệnh Run...</span></div>
<div class="separator" style="clear: both; text-align: left;">
<span style="color: #444444;">Nhập cmd. Bấm Enter.</span></div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPBI06lSQov-9dDv4OE8eMMC5lIUBE5uyX4vfY9oX23K7lE08hs1og3W0ppQx1F5BrNCb47aT8cV9JTNqVYkkHO7TrsRBmP9zKAhc3knpLgsyQ3rysVFboA42PhoGMxs2gECfkbLUupMg/s1600/14-03-2015+7-19-30+SA.jpg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="220" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPBI06lSQov-9dDv4OE8eMMC5lIUBE5uyX4vfY9oX23K7lE08hs1og3W0ppQx1F5BrNCb47aT8cV9JTNqVYkkHO7TrsRBmP9zKAhc3knpLgsyQ3rysVFboA42PhoGMxs2gECfkbLUupMg/s1600/14-03-2015+7-19-30+SA.jpg" width="400" /></a></div>
<div class="separator" style="clear: both; text-align: left;">
<span style="color: #444444; font-family: inherit;">Cửa sổ </span><b style="color: #444444; font-family: inherit;">Command Prompt </b><span style="color: #444444; font-family: inherit;">hiện ra. Tiếp đến gõ lệnh </span><b style="color: #444444; font-family: inherit;">F:</b><span style="color: #444444; font-family: inherit;"> (lưu ý F là ổ USB của bạn) và nhấn Enter để chuyển dấu nhắc sang ổ USB.</span></div>
<div class="separator" style="clear: both;">
<span style="font-family: inherit;"><span style="color: #444444;">Gõ lệnh </span><b><span style="color: #38761d;">attrib -S -H /S /D </span></b><span style="color: #444444;">và nhấn Enter là xong.</span></span></div>
<div class="separator" style="clear: both;">
<span style="font-family: inherit;"><b><span style="color: #0b5394;">Lưu ý:</span></b></span></div>
<div class="separator" style="clear: both;">
<span style="color: #444444; font-family: inherit;">-S để bỏ đi thuộc tính hệ thống bị khóa.</span></div>
<div class="separator" style="clear: both;">
<span style="color: #444444; font-family: inherit;">-H là bỏ đi thuộc tính ẩn bị khóa.</span></div>
<div class="separator" style="clear: both;">
<span style="color: #444444; font-family: inherit;">/S, /D có chức năng thay đổi thuộc tính cho tất cả file, thư mục trong ổ USB.</span></div>
<div class="separator" style="clear: both;">
<b><span style="color: orange;">Cách 3. Sử dụng phần mềm Bkav FixAttrb hoặc USB Show</span></b></div>
<div class="separator" style="clear: both; text-align: center;">
<b><span style="color: #38761d;"><a href="https://drive.google.com/file/d/0B8Hrctiq-vGRUTdFZnhBQjdxc0U/view?usp=sharing" target="_blank" rel="noopener">Download</a></span></b></div>
<div class="separator" style="clear: both; text-align: justify;">
<span style="color: #444444;">Sau khi tải về các bạn chạy file lên và sử dụng, giao diện phần mềm cực kỳ đơn giản như sau:</span></div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKCaLwtPxTig72nH7UqtW8T5myCbaGWieKm7TCJkEPPNS3jG84G_i6G0epYvesOeB-4J9_OEFmreMfEgRoMIdqBPDRJV78zw1wclBdTfwxQskHsg377K_omgm2-lUFq9LlYWqkgqi9r3U/s1600/14-03-2015+7-23-32+SA.jpg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="117" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKCaLwtPxTig72nH7UqtW8T5myCbaGWieKm7TCJkEPPNS3jG84G_i6G0epYvesOeB-4J9_OEFmreMfEgRoMIdqBPDRJV78zw1wclBdTfwxQskHsg377K_omgm2-lUFq9LlYWqkgqi9r3U/s1600/14-03-2015+7-23-32+SA.jpg" width="400" /></a></div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-1jA02Br7oUPB_m-7nPrrmpoKlGwjXBmGcsh2ObonYmffNDewZZXBObMIB0l7BuFVJ7pebVnAVTeI31h9r9qE-JZYGzubsLsYVL2e91xNBgI08ViRtfvF7uN6dJHE8NueCanDCltXE1A/s1600/14-03-2015+7-23-44+SA.jpg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="261" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-1jA02Br7oUPB_m-7nPrrmpoKlGwjXBmGcsh2ObonYmffNDewZZXBObMIB0l7BuFVJ7pebVnAVTeI31h9r9qE-JZYGzubsLsYVL2e91xNBgI08ViRtfvF7uN6dJHE8NueCanDCltXE1A/s1600/14-03-2015+7-23-44+SA.jpg" width="400" /></a></div>
 Chọn thư mục hoặc ổ đĩa cần hiện file ẩn. Ấn OK. Sau đó bấm Hiện file ẩn là xong.<br />
<div class="separator" style="clear: both; text-align: left;">
<img border="0" height="320" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgDB6U3RJPKM2Jqa12OxBWLzgRzQWD5evo5ARckcBVWLiP5aiQr0c5i7zQYuWb4g4fSoiiAXW4WEk9Mc9k2q3DgjU53Et1Znoxqn_97detC42KaXq_fgH9Qvx7_qLVtt-qB5yXiz2fpwOg/s1600/14-03-2015+7-24-03+SA.jpg" width="299" /><img border="0" height="320" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgv1EHZ21t4qKXcsqhdL11UbehuaH8zyIC_8bkuZ8Y0hV89AOLMAZ2B9si7xgH_s65p4qTf-MHI7lZ7P4VX3WgNGrPCIIvZzVX7jryqdfBLlIxHm0hhszB5sYhAvUpMNZSE7rDowBJ1dVM/s1600/14-03-2015+7-24-23+SA.jpg" width="299" /></div>
<div class="separator" style="clear: both; text-align: justify;">
<span style="color: #444444; font-family: inherit;"><strong style="background-attachment: initial; background-clip: initial; background-image: initial; background-origin: initial; background-position: initial; background-repeat: initial; background-size: initial; border: 0px; font-family: inherit; margin: 0px; outline: 0px; padding: 0px;">Với Bkav FixAttrb.exe:</strong> bạn click vào "<strong style="background-attachment: initial; background-clip: initial; background-image: initial; background-origin: initial; background-position: initial; background-repeat: initial; background-size: initial; border: 0px; font-family: inherit; margin: 0px; outline: 0px; padding: 0px;">Chọn ổ đĩa</strong>" để chọn ổ đĩa hoặc thư mục cần hiện các file ẩn rồi bấm "<strong style="background-attachment: initial; background-clip: initial; background-image: initial; background-origin: initial; background-position: initial; background-repeat: initial; background-size: initial; border: 0px; font-family: inherit; margin: 0px; outline: 0px; padding: 0px;">OK</strong>", công cụ báo "<strong style="background-attachment: initial; background-clip: initial; background-image: initial; background-origin: initial; background-position: initial; background-repeat: initial; background-size: initial; border: 0px; font-family: inherit; margin: 0px; outline: 0px; padding: 0px;">Đã đặt xong thuộc tính!</strong>". Lúc này, các bạn đóng cửa sổ công cụ lại, rồi vào ổ đĩa kiểm tra thử xem các file và thư mục bị ẩn giờ đã có thể truy nhập và nhìn thấy dữ liệu bị ẩn trước đó chưa nhé.</span></div>
<div class="separator" style="clear: both; text-align: justify;">
<span style="color: #444444;"><b>Với USB Show.exe:</b> trên giao diện chính bạn bấm nút <b>"Recovery the hide files"</b>, ở cửa sổ <b>"Browse For Folder"</b> tìm chọn ổ đĩa USB mà bạn cần thực hiện, rồi bấm <b>"OK"</b>. Quá trình quét và khôi phục file bị virus ẩn đi sẽ diễn ra sau đó. Đến khi hoàn tất, bạn bấm OK.</span></div>

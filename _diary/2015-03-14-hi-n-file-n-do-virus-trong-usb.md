---
layout: diary_post
title: "Hiện file ẩn do virus trong USB"
date: 2015-03-14T07:47:00.002000+07:00
categories:
  - diary
permalink: /diary/2015/03/14/hi-n-file-n-do-virus-trong-usb/
source_url: "https://phancanhtrinh.blogspot.com/2015/03/hien-file-do-virus-trong-usb.html"
summary: "Virus là một trong những phiền toái lớn của người dùng máy tính; những nỗi khốn đốn này thường đi kèm với anh bạn không thể không nhắc tới là chiếc USB. Lỗi thường gặp nhất là các file trong USB bị sau khi nhiễm virus, nhiều người tá hỏa lên với vấn đề này vì tưởng rằng dữ liệu của họ đã bị gặm nhấm hết. Thật ra các dữ liệu này vẫn còn ở đó chỉ là bị ẩn đi thôi. Đặc điểm các virus này thường khóa luôn chức năng hiện file trong Folder Option nên khó lòng lấy lại được dễ dàng. Những trường hợp cấp"
thumbnail: "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgADy2Iw6PGMrnYFBXEaxfKbqHYyABjMzXLG4N7HbZx4kZ-iju_cmeDjCyBG1bSxE_WHA8126ZuP69jzIaB4bY5s9ZwuaBmoSJlfJ7ZTjsz-Zghm6BY-sf1-5yHfd7x0fm8U8sctapUtDI/s1600/13-03-2015+10-28-46+CH.jpg"
---
Virus là một trong những phiền toái lớn của người dùng máy tính; những nỗi khốn đốn này thường đi kèm với anh bạn không thể không nhắc tới là chiếc USB. Lỗi thường gặp nhất là các file trong USB bị sau khi nhiễm virus, nhiều người tá hỏa lên với vấn đề này vì tưởng rằng dữ liệu của họ đã bị gặm nhấm hết. Thật ra các dữ liệu này vẫn còn ở đó chỉ là bị ẩn đi thôi. Đặc điểm các virus này thường khóa luôn chức năng hiện file trong <b>Folder Option</b> nên khó lòng lấy lại được dễ dàng. Những trường hợp cấp bách như vậy chúng ta có thể áp dụng một số cách sau:

<b>Cách 1. Thử hiện file trong Folder Option</b>

Đặt các thuộc tính như hình bên dưới, lưu ý mục <b>Hide protected operating system files... </b>không được chọn. Cuối cùng nhấn OK và xem kết quả.

<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgADy2Iw6PGMrnYFBXEaxfKbqHYyABjMzXLG4N7HbZx4kZ-iju_cmeDjCyBG1bSxE_WHA8126ZuP69jzIaB4bY5s9ZwuaBmoSJlfJ7ZTjsz-Zghm6BY-sf1-5yHfd7x0fm8U8sctapUtDI/s1600/13-03-2015+10-28-46+CH.jpg" width="305" height="400"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5oVfDNaLQNIyYPgXDNc6-oDuyQHdMlqV7BGdSW_UilZJ-crPIJdmauidrYqfpSuV1PEhhbAW0_kUa0Qwl0NOzivB-HVtLY9_Z-pVRcl5YxCPGG3jKpocwgM_VbNB7U5ncPFxw8fv3wo0/s1600/13-03-2015+10-32-37+CH.jpg" width="328" height="400">

<b></b>

<b>Cách 2. Gõ lệnh hiện file vào cmd</b><br>

Bấm Window + R để mở lệnh Run...

Nhập cmd. Bấm Enter.

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPBI06lSQov-9dDv4OE8eMMC5lIUBE5uyX4vfY9oX23K7lE08hs1og3W0ppQx1F5BrNCb47aT8cV9JTNqVYkkHO7TrsRBmP9zKAhc3knpLgsyQ3rysVFboA42PhoGMxs2gECfkbLUupMg/s1600/14-03-2015+7-19-30+SA.jpg"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPBI06lSQov-9dDv4OE8eMMC5lIUBE5uyX4vfY9oX23K7lE08hs1og3W0ppQx1F5BrNCb47aT8cV9JTNqVYkkHO7TrsRBmP9zKAhc3knpLgsyQ3rysVFboA42PhoGMxs2gECfkbLUupMg/s1600/14-03-2015+7-19-30+SA.jpg" width="400" height="220"></a>

Cửa sổ <b>Command Prompt </b>hiện ra. Tiếp đến gõ lệnh <b>F:</b> (lưu ý F là ổ USB của bạn) và nhấn Enter để chuyển dấu nhắc sang ổ USB.

Gõ lệnh <b>attrib -S -H /S /D </b>và nhấn Enter là xong.

<b>Lưu ý:</b>

-S để bỏ đi thuộc tính hệ thống bị khóa.

-H là bỏ đi thuộc tính ẩn bị khóa.

/S, /D có chức năng thay đổi thuộc tính cho tất cả file, thư mục trong ổ USB.

<b>Cách 3. Sử dụng phần mềm Bkav FixAttrb hoặc USB Show</b>

<b><a href="https://drive.google.com/file/d/0B8Hrctiq-vGRUTdFZnhBQjdxc0U/view?usp=sharing" target="_blank" rel="noopener">Download</a></b>

Sau khi tải về các bạn chạy file lên và sử dụng, giao diện phần mềm cực kỳ đơn giản như sau:

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKCaLwtPxTig72nH7UqtW8T5myCbaGWieKm7TCJkEPPNS3jG84G_i6G0epYvesOeB-4J9_OEFmreMfEgRoMIdqBPDRJV78zw1wclBdTfwxQskHsg377K_omgm2-lUFq9LlYWqkgqi9r3U/s1600/14-03-2015+7-23-32+SA.jpg"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhKCaLwtPxTig72nH7UqtW8T5myCbaGWieKm7TCJkEPPNS3jG84G_i6G0epYvesOeB-4J9_OEFmreMfEgRoMIdqBPDRJV78zw1wclBdTfwxQskHsg377K_omgm2-lUFq9LlYWqkgqi9r3U/s1600/14-03-2015+7-23-32+SA.jpg" width="400" height="117"></a>

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-1jA02Br7oUPB_m-7nPrrmpoKlGwjXBmGcsh2ObonYmffNDewZZXBObMIB0l7BuFVJ7pebVnAVTeI31h9r9qE-JZYGzubsLsYVL2e91xNBgI08ViRtfvF7uN6dJHE8NueCanDCltXE1A/s1600/14-03-2015+7-23-44+SA.jpg"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi-1jA02Br7oUPB_m-7nPrrmpoKlGwjXBmGcsh2ObonYmffNDewZZXBObMIB0l7BuFVJ7pebVnAVTeI31h9r9qE-JZYGzubsLsYVL2e91xNBgI08ViRtfvF7uN6dJHE8NueCanDCltXE1A/s1600/14-03-2015+7-23-44+SA.jpg" width="400" height="261"></a>

 Chọn thư mục hoặc ổ đĩa cần hiện file ẩn. Ấn OK. Sau đó bấm Hiện file ẩn là xong.<br>

<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgDB6U3RJPKM2Jqa12OxBWLzgRzQWD5evo5ARckcBVWLiP5aiQr0c5i7zQYuWb4g4fSoiiAXW4WEk9Mc9k2q3DgjU53Et1Znoxqn_97detC42KaXq_fgH9Qvx7_qLVtt-qB5yXiz2fpwOg/s1600/14-03-2015+7-24-03+SA.jpg" width="299" height="320"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgv1EHZ21t4qKXcsqhdL11UbehuaH8zyIC_8bkuZ8Y0hV89AOLMAZ2B9si7xgH_s65p4qTf-MHI7lZ7P4VX3WgNGrPCIIvZzVX7jryqdfBLlIxHm0hhszB5sYhAvUpMNZSE7rDowBJ1dVM/s1600/14-03-2015+7-24-23+SA.jpg" width="299" height="320">

<strong>Với Bkav FixAttrb.exe:</strong> bạn click vào "<strong>Chọn ổ đĩa</strong>" để chọn ổ đĩa hoặc thư mục cần hiện các file ẩn rồi bấm "<strong>OK</strong>", công cụ báo "<strong>Đã đặt xong thuộc tính!</strong>". Lúc này, các bạn đóng cửa sổ công cụ lại, rồi vào ổ đĩa kiểm tra thử xem các file và thư mục bị ẩn giờ đã có thể truy nhập và nhìn thấy dữ liệu bị ẩn trước đó chưa nhé.

<b>Với USB Show.exe:</b> trên giao diện chính bạn bấm nút <b>"Recovery the hide files"</b>, ở cửa sổ <b>"Browse For Folder"</b> tìm chọn ổ đĩa USB mà bạn cần thực hiện, rồi bấm <b>"OK"</b>. Quá trình quét và khôi phục file bị virus ẩn đi sẽ diễn ra sau đó. Đến khi hoàn tất, bạn bấm OK.

---
layout: post
title: 'Tự động hóa định dạng văn bản với Word [Kỳ 1]'
date: 2015-01-06T23:28:00.001000+07:00
categories:
  - diary
permalink: /diary/2015/01/06/t-ng-h-a-nh-d-ng-v-n-b-n-v-i-word-k-1/
source_url: https://phancanhtrinh.blogspot.com/2015/01/tu-ong-hoa-viec-inh-dang-van-ban-voi.html
---
<div class="separator" style="clear: both; text-align: center;">
</div>
<div class="MsoNormal">
<span style="line-height: 125%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Có lẽ một số bạn rất ghét các tính năng tự động của MS. Word; nhiều khi nó tỏ ra thật phiền toái. Đại loại như tự động đặt Bullet, tự động xuống dòng, tự động thêm dấu cách…<o:p></o:p></span></span></div>
<div class="MsoNormal">
<span style="line-height: 125%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Tuy nhiên, khi thiết kế phần mềm hẳn là nhà sản xuất đã có dụng ý, nghiên cứu kỹ nhu cầu người dùng để đưa ra chúng. Vậy tại sao chúng ta không nghĩ sẽ làm chủ tính năng tự động đó để phục vụ mình một cách tối ưu.<o:p></o:p></span></span></div>
<div class="MsoNormal">
<span style="line-height: 125%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Bài viết sau sẽ trình bày một số thủ thuật để tự động hóa quá trình định dạng văn bản trong MS Word 2013. Sẽ hoàn toàn tương tự cho các phiên bản khác.</span></span></div>
<div class="MsoNormal">
<span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><span style="text-indent: -18pt;"><span style="font-weight: bold; line-height: 125%;">1.</span> </span><b style="text-indent: -18pt;"><span style="line-height: 125%;">Thiết lập lại một số mặc định cơ bản</span></b></span></div>
<div class="MsoNormal">
<b><span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><span style="text-indent: -21.6pt;">1.1. </span><span style="text-indent: -21.6pt;">Thiết lập trang</span></span></b></div>
<div class="MsoNormal">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><b>File/ Print/ Page Setup </b>hoặc nhấp đôi vào <b>thanh Ruler</b> để hiển thị hộp thoại Page Setup. </span></div>
<div class="MsoNormal">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Đặt các thông số cần thiết: Lề và gáy đặt ở Tab Margin; khổ giấy A4 ở Tab Paper. </span></div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjX_Ao5xbyKQ4m2X4XkOahNM6m31Gxe5yCDliR_kp90OmqN7NPNYxcSZND66anlrC4CFLTuemoafl1-lv9CJNBenEGdrgpoWLy5VPmoUjHty_sHgkbcYcjG291eHnjPrVv9XN3i3LZEFx8/s1600/Picture1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjX_Ao5xbyKQ4m2X4XkOahNM6m31Gxe5yCDliR_kp90OmqN7NPNYxcSZND66anlrC4CFLTuemoafl1-lv9CJNBenEGdrgpoWLy5VPmoUjHty_sHgkbcYcjG291eHnjPrVv9XN3i3LZEFx8/s1600/Picture1.png" height="368" width="640" /></span></a></div>
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Lưu ý: Nút <b>Set As Default</b> ở góc trái cuối hộp thoại cho phép mặc định lại các thông số đã đặt cho những file sau này, nếu các thông số sử dụng thường xuyên các bạn có thể nhấn nút này.</span><br />
<a name='more'></a><b><span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.2. Thiết lập font chữ mặc định</span></b><br />
<div class="MsoNormal">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Truy cập Tab<b> Design/ Font/ Customize Font... </b>xuất hiện hộp thoại bên dưới, chọn font chữ bạn cần (thường chúng ta sử dụng Time New Roman, ở đây có 2 ô để mặc định cho tiêu đề và cho nội dung); đặt tên cho định dạng mới này; kích nút <b>Save</b> để lưu lại.</span></div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmfsKLiS1pV6FZ7WYXiVQ9UOnk5juLhg1FQzc60hHBMvPOa8ZKxJHZcdN8pi8RF3Vh_ASnbhjqHeUxsmSIq7KoeEf-WXj1ewezXHFAAOyPd8aN1yTtLKVQ1KGqK1IPCgyX7LoOK5G_e2g/s1600/Picture2.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjmfsKLiS1pV6FZ7WYXiVQ9UOnk5juLhg1FQzc60hHBMvPOa8ZKxJHZcdN8pi8RF3Vh_ASnbhjqHeUxsmSIq7KoeEf-WXj1ewezXHFAAOyPd8aN1yTtLKVQ1KGqK1IPCgyX7LoOK5G_e2g/s1600/Picture2.png" height="364" width="640" /></span></a></div>
<div class="separator" style="clear: both; text-align: center;">
</div>
<div class="MsoNormal">
<b><span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.3. Làm chủ các định dạng mẫu</span></b></div>
<div class="MsoNormal">
<span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.3.1. Tiêu đề</span></div>
<div class="MsoNormal">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Giả sử chúng ta có bố cục bài báo cáo với yêu cầu như sau:</span></div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><span style="line-height: 150%;">1. TIÊU ĐỀ</span><span style="line-height: 150%;"> CẤP 1               : cỡ 16, kiểu hoa, in đậm<o:p></o:p></span></span></div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="line-height: 150%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.1. TIÊU ĐỀ CẤP 2            : cỡ 14, kiểu hoa và đậm<o:p></o:p></span></span></div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="line-height: 150%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.1.1.Tiêu đề cấp 3              : cỡ 14, kiểu thường và đậm<o:p></o:p></span></span></div>
<div class="MsoNormal">
</div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="line-height: 150%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">1.1.1.1.Tiêu đề cấp 4           : cỡ 14,</span></span><span style="line-height: 150%;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"> kiểu thường</span></span></div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;">Đặt con trỏ chuột tại dòng Tiêu đề 1, chọn Numbering với thể loại như hình sau. Tương tự cho tiêu đề cấp 2, 3, 4. Để <b>lùi cấp cho tiêu đề</b>, kích chuột vào Numbering của tiêu đề vừa tạo, nhấn phím <b>Tab</b>.</span></div>
<div class="separator" style="clear: both; text-align: center;">
</div>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgceyqg76dh6mZ6G-qZ8wM7pwAMztiR2AlXQUf3jxcJMFh1dOhV9UEayokZUlaQL4jZKxfoNkHIseMt1d52UMRgs_Ipu7AP4sLiCyMDk_rlQxtK1jaRwCzsPDu_Q7wxMOwQdS_y8Gie0y8/s1600/Picture3.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgceyqg76dh6mZ6G-qZ8wM7pwAMztiR2AlXQUf3jxcJMFh1dOhV9UEayokZUlaQL4jZKxfoNkHIseMt1d52UMRgs_Ipu7AP4sLiCyMDk_rlQxtK1jaRwCzsPDu_Q7wxMOwQdS_y8Gie0y8/s1600/Picture3.png" height="248" width="640" /></span></a></div>
<div class="separator" style="clear: both; text-align: center;">
</div>
<div class="separator" style="clear: both; text-align: center;">
</div>
<div class="MsoNormal" style="line-height: 150%; text-align: left;">
<span style="color: #0b5394; font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-weight: bold; line-height: 150%;">Chìa khóa: </span><span style="color: #20124d; font-family: Helvetica Neue, Arial, Helvetica, sans-serif; line-height: 150%;">MS Word mặc định đằng sau Numbering hay Bullet là một ký tự Tab, do vậy khoảng cách này khá dài và thay đổi bất thường tùy vào chuỗi ký tự theo sau. Cách loại bỏ như sau.</span></div>
<table cellpadding="0" cellspacing="0" class="tr-caption-container" style="margin-left: auto; margin-right: auto; text-align: center;"><tbody>
<tr><td style="text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhzT1ESejktyoByjc6BaBmYkerp4Ry28IBJastaAmVdc1Ur8xkWnijzgVXynXgQbtt1Rw2eXUtdFE_ZRpjiPcgclyf0ZkuKJQgk_H66eK4mu1tiDeQtff011EhVVl22-mwmbggsSkScoq0/s1600/Picture5.png" imageanchor="1" style="margin-left: auto; margin-right: auto;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhzT1ESejktyoByjc6BaBmYkerp4Ry28IBJastaAmVdc1Ur8xkWnijzgVXynXgQbtt1Rw2eXUtdFE_ZRpjiPcgclyf0ZkuKJQgk_H66eK4mu1tiDeQtff011EhVVl22-mwmbggsSkScoq0/s1600/Picture5.png" height="380" width="640" /></span></a></td></tr>
<tr><td class="tr-caption" style="text-align: left;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-size: small;">Đặt lại cách lề cho tiêu đề tùy mục đích của bạn, mình đặt lại 0 cm. </span><br />
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-size: small;">Kích <b>Set for All Levels</b> nếu muốn áp dụng tất cả các cấp.</span></td></tr>
</tbody></table>
<div class="separator" style="clear: both; text-align: center;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtCw0VFnPADkUDjCc3VkSeQ8wASJK-kECKrw_26HGCmt2MK2lZmMkeIFAt9pEoGplk-IPMZk4QCzauJaDqQwePlnw-LrIhcYLzce0ppKKHnwm8bw8HtFPE1CidlmTLCRK7FdzLYSXF5Lk/s1600/Picture6.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgtCw0VFnPADkUDjCc3VkSeQ8wASJK-kECKrw_26HGCmt2MK2lZmMkeIFAt9pEoGplk-IPMZk4QCzauJaDqQwePlnw-LrIhcYLzce0ppKKHnwm8bw8HtFPE1CidlmTLCRK7FdzLYSXF5Lk/s1600/Picture6.png" /></a></div>
<div>
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><span style="line-height: 24px;">Kích nút </span><b style="line-height: 24px;">More/Less</b><span style="line-height: 24px;"> ở góc trái dưới cùng hộp thoại, bạn sẽ thấy phần mở rộng. Chuyển thuộc tính </span><b style="line-height: 24px;">Follow number with:</b><span style="line-height: 24px;"> thành </span><b style="line-height: 24px;">Space </b><span style="line-height: 24px;">(1 dấu cách theo sau Number).</span></span></div>
<div>
<span style="font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif; font-size: small; line-height: 24px;">Sau khi hoàn thành, các bạn tiếp tục định dạng cỡ chữ, màu chữ, font chữ cho tiêu đề nếu cần. Bước tiếp theo là lưu lại mẫu tiêu đề để áp dụng cho các tiêu đề khác. Quá trình được mô tả như sau:</span></div>
<table cellpadding="0" cellspacing="0" class="tr-caption-container" style="margin-left: auto; margin-right: auto; text-align: start;"><tbody>
<tr><td style="text-align: center;"><div style="font-size: 13px; text-align: left;">
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqZIOlx_5BaeBdqKpFr99uncUf61b_48iE9WN9xOtg4TpMbKiXjy6fChGfwxR-cIoni0-FROHldO88COWhCj9ZWpp1EZUb2jnAiNNJ_Ui1ysCucKC4oGyoPMxTYK2oNLbYI0Rj-XBOPik/s1600/Picture9.png" imageanchor="1" style="font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif; margin-left: auto; margin-right: auto; text-align: center;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiqZIOlx_5BaeBdqKpFr99uncUf61b_48iE9WN9xOtg4TpMbKiXjy6fChGfwxR-cIoni0-FROHldO88COWhCj9ZWpp1EZUb2jnAiNNJ_Ui1ysCucKC4oGyoPMxTYK2oNLbYI0Rj-XBOPik/s1600/Picture9.png" height="214" width="640" /></a></div>
</td></tr>
<tr><td class="tr-caption" style="text-align: left;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-size: small;">Chọn tiêu cấp 1 đã định dạng, kích chuột phải vào <b>Heading 1 </b>trên thanh công cụ, chọn <b>Update Heading 1... </b>để lưu lại thuộc tính đã định dạng.</span></td></tr>
</tbody></table>
<table align="center" cellpadding="0" cellspacing="0" class="tr-caption-container" style="margin-left: auto; margin-right: auto; text-align: center;"><tbody>
<tr><td style="text-align: center;"><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh4tcUWu7Zq531ZoKrKTWv3lvid1dnwNqbaYZFCyhyeuRuK7T3evZN9ykzVs3mazl07HgASs324bQHtO-I2039oIS3tAgR9_vEgdm4OLekuL3IfnbGE2DXdShu6N0SraRTs9wEVDwOSYMs/s1600/Picture10.png" imageanchor="1" style="margin-left: auto; margin-right: auto; text-align: center;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif;"><img border="0" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEh4tcUWu7Zq531ZoKrKTWv3lvid1dnwNqbaYZFCyhyeuRuK7T3evZN9ykzVs3mazl07HgASs324bQHtO-I2039oIS3tAgR9_vEgdm4OLekuL3IfnbGE2DXdShu6N0SraRTs9wEVDwOSYMs/s1600/Picture10.png" height="210" width="640" /></span></a></td></tr>
<tr><td class="tr-caption" style="text-align: left;"><span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-size: small;">Di chuyển đến 1 tiêu đề khác cùng cấp kích <b>Heading 1</b> để áp dụng định dạng đã lưu. Làm tương tự cho <b>Heading 2, 3, 4</b>...</span><br />
<div style="text-align: right;">
<span style="font-family: Helvetica Neue, Arial, Helvetica, sans-serif; font-size: small;">[Còn nữa]</span></div>
</td></tr>
</tbody></table>

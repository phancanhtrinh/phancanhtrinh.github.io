---
layout: diary_post
title: "Heading trong Word bị mảng đen biết phải làm sao?"
date: 2018-07-12T16:18:00+07:00
categories:
  - diary
permalink: /diary/2018/07/12/heading-trong-word-b-m-ng-en-bi-t-ph-i-l-m-sao/
source_url: "https://phancanhtrinh.blogspot.com/2018/07/heading-trong-word-bi-mang-en-biet-phai.html"
thumbnail: "http://social.technet.microsoft.com/Forums/getfile/174029"
---
Một ngày đẹp trời Khoá luận của bạn mở lên và Heading bị đen lại.

<img src="http://social.technet.microsoft.com/Forums/getfile/174029" alt="Káº¿t quáº£ hÃ¬nh áº£nh cho Numbering in MS word turned into black boxes" width="640" height="360">

Tốt nhất đập đi làm lại... Lần 1. OK

Lần khác mở lên, đen tiếp... Đập làm lại...

Đã bị thì nó sẽ bị hoài...

Cách giải quyết như sau:

<b>Bước 1: </b>Lưu lại 1 file mới cho chắc ăn

<b>Bước 2:</b> Trên file mới đang mở tạo Macro như sau:

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEidAIMz9GMTkiSqHWYxVAWjalVRX8YEn0Wa8uPBYW2R_Fr-gDT6b7tR6kV6M7xPaXlS5hpjt2yrKcRE-pw3mFPGxExISYCdzExqfb01HOj7XlxupKVsFuwJRZshcW9DnIMfH5e8NTt8Apo/s1600/Screen+Shot+2018-07-12+at+4.10.10+PM.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEidAIMz9GMTkiSqHWYxVAWjalVRX8YEn0Wa8uPBYW2R_Fr-gDT6b7tR6kV6M7xPaXlS5hpjt2yrKcRE-pw3mFPGxExISYCdzExqfb01HOj7XlxupKVsFuwJRZshcW9DnIMfH5e8NTt8Apo/s640/Screen+Shot+2018-07-12+at+4.10.10+PM.png" width="564" height="640"></a>

Chọn tiếp Dấu cộng(+) 

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiY4-ysjVthNtZ8R-5SM2rngDEx_JDk0CXebz2eHWvyFIsM8v3zUCOB7bBAbetVJHusqWmVOQ_u1VLKWDhAPpVuxmSx30AJDx7ci34u3PMKS8sEV_Z0Ts0WyL_qH4QkGDHHaNG2Xq2l8v8/s1600/Screen+Shot+2018-07-12+at+4.10.25+PM.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiY4-ysjVthNtZ8R-5SM2rngDEx_JDk0CXebz2eHWvyFIsM8v3zUCOB7bBAbetVJHusqWmVOQ_u1VLKWDhAPpVuxmSx30AJDx7ci34u3PMKS8sEV_Z0Ts0WyL_qH4QkGDHHaNG2Xq2l8v8/s640/Screen+Shot+2018-07-12+at+4.10.25+PM.png" width="634" height="640"></a>

 Cửa sổ mới như sau:

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgXcTXyo7Kis5L1v3U8h5IPzJLzzoXsfQrpDCRARi3hFZQSlLkUZQ8qjkYIST9zGeoNuuyeYFPXvcR5lKix5C_A2S6xnvBcr4H8YxMeM92gIgMtpx394afHkguZE5vUKmr-PSa2B-koaWg/s1600/Screen+Shot+2018-07-12+at+4.10.37+PM.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgXcTXyo7Kis5L1v3U8h5IPzJLzzoXsfQrpDCRARi3hFZQSlLkUZQ8qjkYIST9zGeoNuuyeYFPXvcR5lKix5C_A2S6xnvBcr4H8YxMeM92gIgMtpx394afHkguZE5vUKmr-PSa2B-koaWg/s640/Screen+Shot+2018-07-12+at+4.10.37+PM.png" width="640" height="286"></a>

 Dán đoạn code sau vào:<br>
<blockquote>

Sub RemoveBlackBox()

'

' RemoveBlackBox Macro

'

'

<br>

For Each templ In ActiveDocument.ListTemplates

For Each lev In templ.ListLevels

lev.Font.Reset

Next lev

Next templ

<br>

<br>

End Sub

</blockquote>
<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhJewA0lvnjmLq-5YoMuV3X9b0Gez62f7Sv4Si0wprNf8QG6UftAdSA2cf7bpz7AQqcVGv6UPJVL3qZKxGoo4-XpxB178im8k_ngBH7bfi-_yIzJSQ1nVNzlSdEPA2_StLMNtw0Yf_fz_Y/s1600/Screen+Shot+2018-07-12+at+4.10.56+PM.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhJewA0lvnjmLq-5YoMuV3X9b0Gez62f7Sv4Si0wprNf8QG6UftAdSA2cf7bpz7AQqcVGv6UPJVL3qZKxGoo4-XpxB178im8k_ngBH7bfi-_yIzJSQ1nVNzlSdEPA2_StLMNtw0Yf_fz_Y/s640/Screen+Shot+2018-07-12+at+4.10.56+PM.png" width="640" height="451"></a><br>
Cuối cùng nhấn Run (Hình tam giác ở góc trái màn hình).

<a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEinWinrqsLTj0fDqmE8ewHVkhLZ72jghF2ZDCbjyCuMyCDlx_ClR3d1y_Eu4gqG_o2-VTkfcGgQXbA2OabXNH2jje9ynChXnByZaNFWrr3FX-Lb7rdHJOOWgTls5JDCbMsvdQgZzEUUSD4/s1600/Screen+Shot+2018-07-12+at+4.11.09+PM.png"><img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEinWinrqsLTj0fDqmE8ewHVkhLZ72jghF2ZDCbjyCuMyCDlx_ClR3d1y_Eu4gqG_o2-VTkfcGgQXbA2OabXNH2jje9ynChXnByZaNFWrr3FX-Lb7rdHJOOWgTls5JDCbMsvdQgZzEUUSD4/s1600/Screen+Shot+2018-07-12+at+4.11.09+PM.png"></a>

Chờ đoạn code chạy xong thì tắt cửa sổ đi là xong!

Tham khảo từ <a href="https://superuser.com/questions/521659/numbering-in-ms-word-turned-into-black-boxes" target="_blank" rel="noopener">superuser.com</a>

<br>

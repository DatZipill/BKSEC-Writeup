# No-main
## Đề bài
Ta được cho 1 file thực thi no-main

## Cách giải
Trước hết em sử dụng xem file thực thi như thế nào bằng lệnh file thì nhận được như sau:
```bash
└─$ file no-main   
no-main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=7be119e8c78aed1cc27b23bfbfdf65918c03e3a0, stripped
```
Em chạy thử bằng kali thì không có gì hiện ra. Vì vậy, em sử dụng Ghidra để phân tích tĩnh. Hàm entry thu được như sau:

![main](main.PNG)

Hai lời gọi hàm đầu là để khởi tạo. Hai hàm sau thì không thể double click vô xem được. Vì thế, em sử dụng gdb để phân tích động 2 hàm này. Trước hết với hàm đầu tiên: 

![ham1](ham1.PNG)

Trong Ghidra, lệnh ASM CALL thanh ghi RBX, ta thấy RBX ở đây có giá trị 0x4013dc, vậy hàm tiếp theo được gọi ở địa chỉ này. Mở lại Ghidra ta tìm được hàm sau: 

![ham1asm](ham1asm.PNG)

Hàm này đọc 1 file có tên input, mà trong thư mục chưa có file nào nên em add thêm 1 file vào để chương trình chạy tiếp.
Tiếp tục đến hàm thứ 2:

![ham2](ham2.PNG)

Thanh ghi RBX lúc này có giá trị là 0x40155a, em sẽ xem trong Ghidra hàm ở vị trí này: 

![](ham2ghidra.PNG)

Hàm này gọi rất nhiều các hàm khác, em xem một số hàm đầu thì nó chỉ return chứ ko có tác dụng gì. Em cho gdb chạy tiếp thì nó trả về exit code 0377. Có lẽ trong số các hàm ở trên có hàm làm chương trình exit. Vì vậy em đặt breakpoint exit 
```bash
b exit
```

rồi cho chạy lại chương trình. Khi chương trình exit, em dùng lệnh 
```bash 
bt
```

để xem lại địa chỉ câu lệnh trước khi chương trình bị exit. Địa chỉ ta thu được là 0x0000000000402815 nên em đặt thêm 1 breakpoint ở 0x0000000000402810. Khi hit breakpoint tại đây, em xem các lệnh tiếp theo của thanh ghi RIP thì thu được như sau:

![](hamkey.PNG)

Đây chính là hàm xử lí flag của mình. Hàm FUN kia so sánh các giá trị của local_68..., nếu sai thì sẽ exit -1. Đến đây em sử dụng Z3 để giải và tìm ra được flag

CyKor{Sorry_for_the_prank_but_wasn't_it_fun?_e071a0b358c7a6c4e4}


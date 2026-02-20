
.data
nilai:  .word 0      
dummy:  .word 0      
data1:  .word 7      
hasil:  .word 0      

.text
.globl main

main:
    li  $s0, 0x10010000   
    li  $t2, 3             

    lw  $t0, 8($s0)        # ambil data1 (7)
    add $t1, $t0, $t2      # t1 = 7 + 3
    sw  $t1, 12($s0)       

    li $v0, 10
    syscall
.data
w0: .word 4
w1: .word 18
w2: .word 0
m1: .word 0
m2: .word 0
m3: .word 0
A: .word 12

.text
.globl main
main:
    lw   $s0, w1        
    lw   $s1, w2        

    lw   $t0, w0        
    lw   $t1, A         
    add  $s2, $t0, $t1  

    add  $s3, $s0, $s1  
    add  $s3, $s3, $s2  

    sw   $s3, m1       
    lw   $v0, m1       

    sw   $v0, m2
    sw   $s2, m3       

    li $v0, 10
    syscall
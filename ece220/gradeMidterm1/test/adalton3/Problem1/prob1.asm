.ORIG x3000

AND R0, R0, #0    ; clear R0
LDI R1, X_LOC     ; R1 <- x
NOT R2, R1
ADD R2, R2, #1    ; R2 <- negative x
ADD R3, R0, #1    ; R3 <- i = 1

LOOP ADD R4, R3, R2   ; If i < x
     BRzp END

     NOT R5, R3
     ADD R5, R5, #1   ; R5 <- negative i
     ADD R4, R5, R1   ; R4 <- x - i

     ADD R5, R4, R5   ; if i <= x - i
     BRn CONT

     ADD R0, R3, #0   ; Print i
     JSR PRINT_HEX
     LD R0, SPACE     ; Print space
     OUT
     ADD R0, R4, #0   ; Print x - i
     JSR PRINT_HEX
     LD R0, NEWLINE   ; Print new line
     OUT

CONT ADD R3, R3, #1   ; Increment i
     BRnzp LOOP

END HALT

PRINT_HEX
    ST R0, SAVE_R0
    ST R3, SAVE_R3
    ST R4, SAVE_R4
    ST R5, SAVE_R5
    ST R6, SAVE_R6
    ST R7, SAVE_R7

    ADD R3, R0, #0
    AND R5,R5,#0
DIG_LOOP
    AND R4,R4,#0
    AND R0,R0,#0
BIT_LOOP
    ADD R0,R0,R0
    ADD R3,R3,#0
    BRzp MSB_CLEAR
    ADD R0,R0,#1
MSB_CLEAR
    ADD R3,R3,R3
    ADD R4,R4,#1
    ADD R6,R4,#-4
    BRn BIT_LOOP

    ADD R6,R0,#-10
    BRzp HIGH_DIGIT
    LD R6, ASCII_0
    BRnzp PRINT_DIGIT
HIGH_DIGIT
    LD R6,ASC_HIGH
PRINT_DIGIT
    ADD R0,R0,R6
    OUT

    ADD R5,R5,#1
    ADD R6,R5,#-4
    BRn DIG_LOOP

    LD R0, SAVE_R0
    LD R3, SAVE_R3
    LD R4, SAVE_R4
    LD R5, SAVE_R5
    LD R6, SAVE_R6
    LD R7, SAVE_R7
    RET

SAVE_R0     .BLKW #1
SAVE_R3     .BLKW #1
SAVE_R4     .BLKW #1
SAVE_R5     .BLKW #1
SAVE_R6     .BLKW #1
SAVE_R7     .BLKW #1
ASC_HIGH    .FILL x0037
X_LOC       .FILL x5000
SPACE       .FILL x0020
NEWLINE     .FILL x000A
ASCII_0     .FILL x0030

.END


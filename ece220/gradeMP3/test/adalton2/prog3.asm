;Assuming user will only enter ' ' 0-9 *+/-
;
;
;
.ORIG x3000
	LD	R2, STR_ADDR		;store the decode string at x4000
	AND R0, R0, #0			;
	ADD R0, R0, #0			;
	AND R4, R4, #0			;
GET_NEXT_CHAR
	GETC				;
	OUT
	ADD R3, R0, #0			;
	NOT R3, R3			;
	ADD R3, R3, #1
	LD R1, NEW_LINE			;
	ADD R5, R1, R3			;
	BRz DONE			;if '/n' branch to done
	LD R1, CHAR_RETURN		;
	ADD R5, R1, R3			;
	BRz DONE			;if '/r' branch to done
	LD	R1, SPACE		;
	ADD R5, R1, R3			;
	BRz FIND_SPACE
	JSR DECODE			;
	;ADD R4, R0, #0			;for multi-digit comment this line and uncomment next two lines
	JSR MULT_TEN
	ADD R4, R0, R4
	BRnzp GET_NEXT_CHAR		;
FIND_SPACE
	STR R4, R2, #0
	ADD R2, R2, #1			;increment str_add pointer
	AND R4, R4, #0
	BRnzp GET_NEXT_CHAR		;
DONE
	LD R4, NEW_LINE			;
	NOT R4, R4
	ADD R4, R4, #1
	STR R4, R2, #0
	LD R1, STR_ADDR
	JSR EVALUATE
	
	HALT

STR_ADDR	.FILL x5000		
SPACE	.FILL x0020
NEW_LINE	.FILL x000A
CHAR_RETURN	.FILL x000D


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;find the real value of operand, or keep the ascii value if operator
;input - R0 holds the input
;output - R0
DECODE
	ST R1, DECODE_R1		;callee-saved reg
	ST R5, DECODE_R5		;callee-saved	reg
	ST R7, DECODE_R7
	LD R1, NINE
	NOT R1, R1
	ADD R1, R1, #1
	ADD R5, R0, R1
	BRp EXPO
	LD R1, 	ZERO			;
	NOT R1, R1			;
	ADD R1, R1, #1			;
	ADD R5, R0, R1			;
	BRn OPERATOR			;	
	ADD R0, R5, #0			; if number, move that number to R0
	BRnzp DECODE_DONE
OPERATOR
	NOT R0, R0
	ADD R0, R0, #1
	LD R1, OP_ADD
	ADD R5, R1, R0
	BRz DECODE_DONE
	LD R1, OP_MIN
	ADD R5, R1, R0
	BRz DECODE_DONE
	LD R1, OP_MUL
	ADD R5, R1, R0
	BRz DECODE_DONE
	LD R1, OP_DIV
	ADD R5, R1, R0
	BRz DECODE_DONE
	BRnzp DE_ERR
EXPO	NOT R0, R0
	ADD R0, R0, #1
	LD R1, OP_EXP
	ADD R5, R1, R0
	BRz DECODE_DONE
DE_ERR	LEA R0, ERR_MSG
	PUTS
	AND R0, R0, #0
DECODE_DONE
	LD R1, DECODE_R1		;
	LD R5, DECODE_R5		;
	LD R7, DECODE_R7
	RET


DECODE_R1	.BLKW #1	;
DECODE_R5	.BLKW #1	;
DECODE_R7	.BLKW #1
OP_ADD		.FILL x002B
OP_MIN		.FILL x002D
OP_DIV		.FILL x002F
OP_MUL		.FILL x002A
OP_EXP		.FILL x005E
ZERO	.FILL x0030
NINE	.FILL x003A
ERR_MSG	.STRINGZ "\nError invalid input"





;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;R4 <- R4*10
;input R4
;output R4
MULT_TEN
	ST R1, MULT_TEN_R1	;
	ST R2, MULT_TEN_R2	;
	LD R1, TEN		;
	AND R2, R2, #0		;
MULT_LOOP
	ADD R2, R2, R4		;
	ADD R1, R1, #-1		;
	BRp MULT_LOOP		;
	ADD R4, R2, #0		;
	LD R1, MULT_TEN_R1	;
	LD R2, MULT_TEN_R2	;
	RET

MULT_TEN_R1	.BLKW #1	;
MULT_TEN_R2	.BLKW #1	;
TEN	.FILL x000A	;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;R1 - start address of the expression string
;R6 - the numerical value of the end result
;
;
EVALUATE
	ST R0, EVAL_R0
	ST R1, EVAL_R1
	ST R2, EVAL_R2
	ST R3, EVAL_R3
	ST R4, EVAL_R4
	ST R5, EVAL_R5
	ST R7, EVAL_R7
EVAL_LOOP
	LDR R0, R1, #0
	BRn E_OP
	JSR PUSH
	ADD R5, R5, #0
	BRp EVAL_WRONG
	ADD R1, R1, #1
	BRnzp EVAL_LOOP	
E_OP	ADD R2, R0, #0		
	ADD R5, R2, #10		
	BRz EVAL_DONE
	JSR POP
	ADD R5, R5, #0
	BRp EVAL_WRONG
	ADD R3, R0, #0
	JSR POP
	ADD R5, R5, #0
	BRp EVAL_WRONG
	ADD R4, R0, #0
	LD R5, ASCII_PLUS
	ADD R5, R2, R5
	BRz PLUS_OP
	LD R5, ASCII_MIN
	ADD R5, R2, R5
	BRz MIN_OP
	LD R5, ASCII_MUL
	ADD R5, R2, R5
	BRz MUL_OP
	LD R5, ASCII_DIV
	ADD R5, R2, R5
	BRz DIV_OP
	LD R5, ASCII_EXP
	ADD R5, R2, R5
	BRz EXP_OP
PLUS_OP	JSR PLUS
	JSR PUSH
	ADD R1, R1, #1
	BRnzp EVAL_LOOP
MIN_OP	JSR MIN
	JSR PUSH
	ADD R1, R1, #1
	BRnzp EVAL_LOOP
MUL_OP	JSR MUL
	JSR PUSH
	ADD R1, R1, #1
	BRnzp EVAL_LOOP
DIV_OP	JSR DIV
	JSR PUSH
	ADD R1, R1, #1
	BRnzp EVAL_LOOP
EXP_OP
	JSR EXP
	JSR PUSH
	ADD R1, R1, #1
	BRnzp EVAL_LOOP
EVAL_DONE
	JSR POP
	ADD R5, R5, #0
	BRp EVAL_WRONG
	ADD R6, R0, #0
	JSR POP
	ADD R5, R5, #0
	BRp EVAL_CORRECT
EVAL_WRONG
	LEA R0, EVAL_ERR
	PUTS
EVAL_CORRECT
	LD R0, EVAL_R0
	LD R1, EVAL_R1
	LD R2, EVAL_R2
	LD R3, EVAL_R3
	LD R4, EVAL_R4
	LD R5, EVAL_R5
	LD R7, EVAL_R7
	RET

EVAL_R0		.BLKW #1
EVAL_R1		.BLKW #1
EVAL_R2		.BLKW #1
EVAL_R3		.BLKW #1
EVAL_R4		.BLKW #1
EVAL_R5		.BLKW #1
EVAL_R7		.BLKW #1
ASCII_PLUS	.FILL x002B
ASCII_MIN	.FILL x002D
ASCII_MUL	.FILL x002A
ASCII_DIV	.FILL x002F
ASCII_EXP	.FILL x005E
EVAL_ERR	.STRINGZ "\nInvalid Expression!"


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;input R3, R4
;out R0
PLUS	ADD R0, R3, R4
	RET
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;input R3, R4
;out R0
MIN	NOT R3, R3
	ADD R3, R3, #1
	ADD R0, R3, R4
	RET
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;input R3, R4
;out R0
MUL	AND R0, R0, #0
MUL_LOOP
	ADD R0, R4, R0
	ADD R3, R3, #-1
	BRp MUL_LOOP
	RET
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;input R3, R4
;out R0
DIV	AND R0, R0, #0
	NOT R3, R3
	ADD R3, R3, #1
	ADD R0, R0, #-1
DIV_LOOP
	ADD R0, R0, #1
	ADD R4, R4, R3
	BRzp DIV_LOOP
	RET
	
	
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;input R3, R4
;out R0
EXP	ST R1, EXP_R1
	ST R2, EXP_R2
	ST R7, EXP_R7
	ADD R1, R3, #-1
	ADD R2, R4, #0
	ADD R3, R2, #0
EXP_LOOP
	ADD R4, R2, #0
	JSR MUL
	ADD R3, R0, #0
	ADD R1, R1, #-1
	BRp EXP_LOOP
	LD R1, EXP_R1
	LD R2, EXP_R2
	LD R7, EXP_R7
	RET
EXP_R1	.BLKW #1
EXP_R2	.BLKW #1
EXP_R7	.BLKW #1
;IN:R0, OUT:R5 (0-success, 1-fail/overflow)
;R3: STACK_END R4: STACK_TOP
;
PUSH	
	ST R3, PUSH_SaveR3	;save R3
	ST R4, PUSH_SaveR4	;save R4
	AND R5, R5, #0		;
	LD R3, STACK_END	;
	LD R4, STACk_TOP	;
	ADD R3, R3, #-1		;
	NOT R3, R3		;
	ADD R3, R3, #1		;
	ADD R3, R3, R4		;
	BRz OVERFLOW		;stack is full
	STR R0, R4, #0		;no overflow, store value in the stack
	ADD R4, R4, #-1		;move top of the stack
	ST R4, STACK_TOP	;store top of stack pointer
	BRnzp DONE_PUSH		;
OVERFLOW
	ADD R5, R5, #1		;
DONE_PUSH
	LD R3, PUSH_SaveR3	;
	LD R4, PUSH_SaveR4	;
	RET


PUSH_SaveR3	.BLKW #1	;
PUSH_SaveR4	.BLKW #1	;


;OUT: R0, OUT R5 (0-success, 1-fail/underflow)
;R3 STACK_START R4 STACK_TOP
;
POP	
	ST R3, POP_SaveR3	;save R3
	ST R4, POP_SaveR4	;save R3
	AND R5, R5, #0		;clear R5
	LD R3, STACK_START	;
	LD R4, STACK_TOP	;
	NOT R3, R3		;
	ADD R3, R3, #1		;
	ADD R3, R3, R4		;
	BRz UNDERFLOW		;
	ADD R4, R4, #1		;
	LDR R0, R4, #0		;
	ST R4, STACK_TOP	;
	BRnzp DONE_POP		;
UNDERFLOW
	ADD R5, R5, #1		;
DONE_POP
	LD R3, POP_SaveR3	;
	LD R4, POP_SaveR4	;
	RET


POP_SaveR3	.BLKW #1	;
POP_SaveR4	.BLKW #1	;
STACK_END	.FILL x3FF0	;
STACK_START	.FILL x4000	;
STACK_TOP	.FILL x4000	;


.END

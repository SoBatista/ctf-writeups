"""
Stack frame layout (conceptually):

[  local4 ]  <--- ebp-0x10
[  local3 ]  <--- ebp-0x0c
[  local2 ]  <--- ebp-0x08
[  local1 ]  <--- ebp-0x04
[   ebp   ]
[   ret   ]  <--- ebp+0x04
[   arg1  ]  <--- ebp+0x08
[   arg2  ]  <--- ebp+0x0c
"""

def asm2(arg1, arg2):
    # mov eax, [ebp+0xc]  -> local1 = arg2
    local1 = arg2

    # mov eax, [ebp+0x8]  -> local2 = arg1
    local2 = arg1

    # loop: while(local2 <= 0x2d12)
    while local2 <= 0x2d12:
        local1 += 1      # add [ebp-0x4], 0x1
        local2 += 0x9f   # add [ebp-0x8], 0x9f

    return hex(local1)

print(asm2(0x6, 0x21))

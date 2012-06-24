##
## bitlets
##

### main()
    #ESCAPE_CODE = escapeCharToKey(ESCAPE_CHAR)

### parseCmdLine()
#     parser.add_option("-c", "--cmdkey", dest="cmdkey",
#                       default="^Aa", help="Screen cmdkey. See screen manpage.")


# ESCAPE_CHAR = '\\'
# PASS_CHAR = '\\'
# ESCAPE_CODE = None
# HIDE_CMD = 'h'

# hidden = True
# esc_found = 0

# def filterInput(buff):
#     global hidden, esc_found
#     out = []
#     print "filterInput in:", esc_found, hidden, buff
#     for char in buff:
#         if char == ESCAPE_CODE:
#             esc_found = esc_found + 1
#         elif char == PASS_CHAR:
#             if esc_found % 2 == 1:
#                 esc_found = esc_found + 1
#             else:
#                 esc_found = 0
#         elif esc_found == 1:
#             if char == HIDE_CMD:
#                 # Eat this cmd sequence
#                 if hidden:
#                     hidden = False
#                     print "Unhiding screen"
#                 else:
#                     hidden = True
#                     print "Hiding screen"
#                 out = out[:len(out) - 1]
#                 esc_found = 0
#                 continue
#             elif hidden:
#                 # extra escape it
#                 out.append(PASS_CHAR)
#                 out.append(ESCAPE_CODE)
#             esc_found = 0
#         elif (esc_found > 1) and (esc_found % 2 == 0):
#             if hidden:
#                 out.append(ESCAPE_CODE)
#                 out.append(PASS_CHAR)
#             esc_found = 0
#         out.append(char)
#     print "out array", out
#     out = "".join(out)
#     print "filterInput out:", out
#     return out

# def escapeCharToKey(char):
#     c = ord(char)
#     if ((c >= 'a') and (c <= 'z')):
#         return chr(1 + c - 'a')
#     else:
#         if char == '@':
#             return chr(0x00)
#         elif char == '[':
#             return chr(0x1b)
#         elif char == '\\':
#             return chr(0x1c)
#         elif char == ']':
#             return chr(0x1d)
#         elif char == '^':
#             return chr(0x1e)
#         elif char == '_':
#             return chr(0x1f)
#         else:
#             raise Exception("Unknown control character: %s" % char)


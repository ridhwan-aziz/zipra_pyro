"""Text Parser

Parse incoming message text and get the detected command and its arguments"""


class RequestedCmd:
    def __init__(self, prefix: str|None, cmd: str|None, username: str|None):
        self.username = username
        self.cmd = cmd
        self.prefix = prefix
        # Aliases
        self.uname = self.username
        self.command = self.cmd
    
    @property
    def raw_cmd(self):
        if not self.cmd:
            return None
        command = f"{self.prefix}{self.command}"
        if self.username != None:
            command += '@' + self.username
        return command

class CuttedArgument:
    def __init__(self, origin: str, cut: list[dict[str, int]], replaced: str):
        self.origin = origin
        self.cut = cut
        self.replaced = replaced


class Arguments:
    def __init__(self, arguments: str):
        self.arguments = arguments
        # Alias
        self.args = self.arguments


    def cut(self, n: int) -> CuttedArgument|None:
        text = self.args
        original = text
        if text is None:
            return None
        split = text.split()

        # Get n first from splitted
        n_get = split[:n]
        
        current_pos = 0
        cut = []
        for string in n_get:
            len_text = len(text)
            text = text.lstrip()
            len_strip = len_text - len(text)
            found = text.find(string)
            cut.append({'text': string, 'position': current_pos})
            length = len(string)
            current_pos += length + len_strip
            text_to_replace = text[found:found + length]
            text = text.replace(text_to_replace, '', 1)

        return CuttedArgument(original, cut, text)


class ParserResult:
    def __init__(self, text: str|None, req: RequestedCmd|None, args: Arguments|None):
        self.req = req
        self.args = args
        # Aliases
        self.request = self.req
        self.arguments = self.args


class Parser:
    def __init__(self, bot_username: str):
        self.username = bot_username
        self.prefixes = ['/', '!', '$', '.', '\\', '~']


    def parse(self, text: str):
        # Setting up needed variables
        split = text.lower().split()
        cmd = None
        args = None

        # Getting command
        f_split = split[0]
        prefix = f_split[0]
        if prefix not in self.prefixes:
            cmd = RequestedCmd(None, None, None)
            args = Arguments(None)
        else:
            r_string = f_split.replace('prefix', '', 1)
            tag_split = r_string.split("@")
            if len(tag_split) <= 1:
                cmd = RequestedCmd(prefix, tag_split[0][1:], None)
                args = Arguments(text[len(tag_split[0]):].strip())
            elif tag_split[1] == self.username:
                cmd = RequestedCmd(prefix, tag_split[0][1:], tag_split[1])
                args = Arguments(text[len(tag_split[0]+'@'+tag_split[1]):].strip())
            else:
                cmd = RequestedCmd(None, None, None)
                args = Arguments(None)

        return ParserResult(text, cmd, args)
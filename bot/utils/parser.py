"""Text Parser

Parse incoming message text and get the detected command and its arguments"""


class RequestedCmd:
    def __init__(self, prefix: str | None, cmd: str | None, username: str | None):
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
        if self.username is not None:
            command += '@' + self.username
        return command

    def to_dict(self):
        return {'request': self.command, 'username': self.username, 'prefix': self.prefix, 'raw_cmd': self.raw_cmd}


class CutArgumentResult:
    def __init__(self, origin: str | None, cut: list[dict[str, int]] | None, replaced: str | None):
        self.origin = origin
        self.cut = cut
        self.replaced = replaced


class Arguments:
    def __init__(self, arguments: str | None, distance: int | None):
        self.arguments = arguments if arguments else None
        self.dist = distance
        # Alias
        self.args = self.arguments

    def cut(self, n: int) -> CutArgumentResult | None:
        text = self.args
        original = text
        if text is None:
            return CutArgumentResult(None, None, None)
        split = text.split()

        # Get n first from split
        n_get = split[:n]

        current_pos = 0
        cut = []
        for string in n_get:
            len_text = len(text)
            print(text)
            print(len(text))
            text = text.lstrip()
            print(len(text))
            print(text)
            len_strip = len_text - len(text)
            found = text.find(string)
            current_pos += len_strip
            cut.append({'text': string, 'position': current_pos})
            length = len(string)
            current_pos += length
            text_to_replace = text[found:found + length]
            text = text.replace(text_to_replace, '', 1)
            print(text)

        return CutArgumentResult(original, cut, text)

    def to_dict(self):
        cut = self.cut(4096)
        return {'arguments': self.args, 'cut_all': {'origin': cut.origin, 'cut': cut.cut}, 'range_to_cmd': self.dist}


class ParserResult:
    def __init__(self, text: str | None, req: RequestedCmd | None, args: Arguments | None):
        self.text = text
        self.req = req
        self.args = args
        # Aliases
        self.txt = self.text
        self.request = self.req
        self.arguments = self.args


class Parser:
    def __init__(self, bot_username: str):
        self.username = bot_username
        self.prefixes = ['/', '!', '$', '.', '\\', '~']

    def parse(self, text: str):
        # Setting up needed variables
        split = text.lower().split()

        # Getting command
        f_split = split[0]
        prefix = f_split[0]
        if prefix not in self.prefixes:
            cmd = RequestedCmd(None, None, None)
            args = Arguments(None, None)
        else:
            r_string = f_split.replace('prefix', '', 1)
            tag_split = r_string.split("@")
            if len(tag_split) <= 1:
                cmd = RequestedCmd(prefix, tag_split[0][1:], None)
                to_replace = tag_split[0]
                replace = text.replace(to_replace, '', 1)
                dist = len(replace) - len(replace.lstrip())
                args = Arguments(text[len(to_replace):].strip(), dist)
            elif tag_split[1] == self.username:
                cmd = RequestedCmd(prefix, tag_split[0][1:], tag_split[1])
                to_replace = tag_split[0] + '@' + tag_split[1]
                replace = text.replace(to_replace, '', 1)
                dist = len(replace) - len(replace.lstrip())
                args = Arguments(text[len(to_replace):].strip(), dist)
            else:
                cmd = RequestedCmd(None, None, None)
                args = Arguments(None, None)

        return ParserResult(text, cmd, args)

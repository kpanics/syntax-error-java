import re


class SimpleJavaLexer:
    def __init__(self):
        self.patterns = [
            (r'\b(public|private|protected|static|void|class|interface|extends|implements)\b', 'KEYWORD'),
            (r'\b(int|double|boolean|char|String|List|Map)\b', 'TYPE'),
            (r'\b(if|else|for|while|return|new|this|super)\b', 'CONTROL'),
            (r'@\w+', 'ANNOTATION'),
            (r'//.*', 'COMMENT'),
            (r'/\*.*?\*/', 'COMMENT_MULTILINE'),
            (r'"[^"]*"', 'STRING'),
            (r'\b\d+\b', 'NUMBER'),
        ]
        self.colors = {
            'KEYWORD': (204, 120, 50),  # оранжевый
            'TYPE': (152, 118, 170),  # фиолетовый
            'CONTROL': (86, 156, 214),  # синий
            'ANNOTATION': (255, 198, 109),  # желтый
            'COMMENT': (106, 153, 85),  # зеленый
            'COMMENT_MULTILINE': (106, 153, 85),
            'STRING': (206, 145, 120),  # коричневый
            'NUMBER': (181, 206, 168),  # светло-зеленый
            'DEFAULT': (212, 212, 212),  # серый (обычный текст)
        }

    def tokenize(self, code: str) -> list:
        tokens = []
        for line in code.split('\n'):
            line_tokens = []
            pos = 0
            while pos < len(line):
                match = None
                for pattern, token_type in self.patterns:
                    regex = re.compile(pattern)
                    match = regex.match(line, pos)
                    if match:
                        line_tokens.append((match.group(), token_type, pos))
                        pos = match.end()
                        break
                if not match:
                    line_tokens.append((line[pos], 'DEFAULT', pos))
                    pos += 1
            tokens.append(line_tokens)
        return tokens
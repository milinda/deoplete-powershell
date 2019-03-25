import json
import re
import os
from .base import Base
from deoplete.util import debug, getlines


script_dir = os.path.dirname(os.path.realpath(__file__))

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'powershell'
        self.mark = '[powershell]'
        self.filetypes = ['ps1']
        self.rank = 500
        self.current = vim.current
        self.vim = vim
        self.cmdlets = []
        self.cmdlets_to_params = {}
        self.previous_cmdlet_suggestions = []
        self.previous_param_suggestions = []

    def on_init(self, context):
        init_kb('{}/{}'.format(script_dir, 'ps-commands.json'))

    def gather_candidates(self, context):
        current = context['complete_str']
        line = context['position'][1]
        line_text = getlines(self.vim, line, line)[0]
       
        if current.startswith('-'):
            if not self.previous_cmdlet_suggestions:
                return []
            else:
                for cmdlet in self.previous_cmdlet_suggestions:
                    if re.findall('\\b{}\\b'.format(cmdlet), line_text):
                        params = self.cmdlets_to_params[cmdlet]
                        candidates = [p for p in params if current.lower() in p.lower()]
        else:
            candidates = [c for c in self.cmdlets if current.lower() in c.lower()]
            self.previous_cmdlet_suggestions = candidates

        if not candidates:
            return []
        else:
            out = []
            for c in candidates:
                out.append(dict(word=c,abbr=c,info='',dup=1))

            return out

    def init_kb(self, kb_path):
        with open(kb_path, 'rb') as f:
            cmdlets_info = json.load(f)
            for cmdlet in [*cmdlets_info]:
                self.cmdlets.append(cmdlet)
                self.cmdlets_to_params[cmdlet] = cmdlets_info[cmdlet]


            





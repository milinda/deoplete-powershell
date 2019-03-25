from .base import Base
from deoplete.util import debug, getlines


class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'powershell'
        self.mark = '[powershell]'
        self.filetypes = ['ps1']
        self.rank = 500
        self.current = vim.current
        self.vim = vim
        self.kb = None

    def on_init(self, context):
        kb_path = self.vim.eval('deoplete#sources#powershell#kb')
        self.init_kb(kb_path)

    def gather_candidates(self, context):
        current = context['complete_str']
        line = context['position'][1]
        line_text = getlines(self.vim, line, line)[0]
        
        debug(self.vim, '{}:{}:{}'.format(current, line, line_text)
        
        return ['Get-AzureRmResource', 'Get-AzureADUser']

    def init_kb(self, kb_path):
        pass





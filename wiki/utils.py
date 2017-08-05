class Indexer:
    def __init__(self, index_fname, redirect_fname):
        self._word2index = self._load_index(index_fname)
        self._redirect = self._load_redirect(redirect_fname)
        
    def _load_index(self, fname):
        try:
            with open(fname, encoding='utf-8') as f:
                return {r.split('\t')[0]:r.split('\t')[1].strip() for r in f}
        except Exception as e:
            print(e)
            return {}
        
    def _load_redirect(self, fname):
        try:
            with open(fname, encoding='utf-8') as f:
                return {r.split('\t>\t')[0]:r.split('\t>\t')[1].strip() for r in f if len(r.split('\t>\t')) == 2}
        except Exception as e:
            print(e)
            return {}
        
    def __call__(self, query):
        return self.find(query)
        
    def find(self, query):
        retrieves = {}
        if query in self._word2index:
            retrieves['match'] = self._word2index[query]
        redirected = self.redirect(query)
        if redirected != query:
            retrieves['redirect'] = redirected
        similars = set()
        for key in self._word2index:
            if query in key and query != key:
                redirected = self.redirect(key)
                similars.add(redirected)
        if similars:
            retrieves['similars'] = similars
        return retrieves
    
    def redirect(self, query):
        q = query
        while (q in self._redirect):
            q = self._redirect[q]
        return q
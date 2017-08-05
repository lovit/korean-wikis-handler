import re

url_pattern = re.compile('http[s]?://[\w./?=#&%]+')
link_pattern = re.compile('\[\[[\w()/.:|\s]+\]\]')
url_pattern = re.compile('http[s]?://[\w./?=#&%]+')

def get_links(doc):
    links = {link[2:].split('|')[0].replace(']]', '') for link in link_pattern.findall(doc)}
    links = {link for link in links if not (url_pattern.match(link))}    
    links = {link.strip().replace('분류:','') for link in links}
    return links

def get_hierarchy(doc):
    clean = lambda link: link.replace('[','').replace(']','')    
    lines = doc.split('\n')
    parents = {clean(link) for line in lines for link in link_pattern.findall(line) if ' * 상위 문서 :' in line}
    children = {clean(link) for line in lines for link in link_pattern.findall(line) if ' * 하위 문서 :' in line}
    relateds = {clean(link) for line in lines for link in link_pattern.findall(line) if ' * 관련 문서 :' in line}
    category = {clean(link.replace('분류:', '')).strip() for line in lines for link in link_pattern.findall(line) if '분류:' in line}
    return parents, children, relateds, category

def get_text(doc):
    is_table = lambda line: '||' in line
    is_include = lambda line: '[include(' in line
    def clean(line):
        line = line.replace("'''", "").replace('|',' ').replace('[*', '').replace('[','').replace(']','').replace('=','').replace('\\','').replace('-', '').replace('~','').replace('(...)','.')
        line = line.replace("\'", "'")
        for url in url_pattern.findall(line):
            line = line.replace(url, ' ')
        if line and (line[0] == '>' or line[0] == '*'): line = line[1:]
        return line.strip()
    
    return [clean(line) for line in doc.split('\n') if (not is_include(line)) and (not is_table(line))]

def to_graph(namuwiki, verbose=True):
    import sys
    graph = {}
    
    for i, entity in enumerate(namuwiki):
        if verbose and (i+1) % 10000 == 0:
            sys.stdout.write('\r  ... to graph (%d in %d)' % (i+1, len(namuwiki)))
        title = entity.get('title', '')
        if not title: continue
        
        title_lower = title.lower()
        if '.jpg' in title_lower or '.gif' in title_lower or '.png' in title_lower:
            continue
        
        links = get_links(entity.get('text', ''))
        if links:
            linked_entities = graph.get(title, set())
            linked_entities.update(links)
            graph[title] = linked_entities
    if verbose:
        sys.stdout.write('\ndone')
    return graph

def to_text(namuwiki, directory, max_num_files=10000, debug=True, verbose=True):
    import os
    import sys
    n_saved = 0
    subdirectory = 0
    
    if debug:
        max_num_files = 50
    
    if not os.path.exists('%s/0/' % directory):
        os.makedirs('%s/%d/' % (directory, subdirectory))
    
    with open('%s/index.txt' % directory, 'w', encoding='utf-8') as fi:
        with open('%s/redirect.txt' % directory, 'w', encoding='utf-8') as fr:
            for i, entity in enumerate(namuwiki):
                if verbose and (i+1) % 1000 == 0:
                    sys.stdout.write('\r  ... to text (%d in %d)' % (i+1, len(namuwiki)))

                doc = entity.get('text', '')
                text = '\n'.join(get_text(doc)).strip()
                if not text:
                    continue
                    
                title = entity.get('title', '')
                if text[:9] == '#redirect':
                    fr.write('%s\t>\t%s\n' % (title, text[10:].strip()))
                    continue

                with open('%s/%d/%d.txt' % (directory, subdirectory, n_saved), 'w', encoding='utf-8') as fo:
                    fo.write('%s\n' % text)

                fi.write('%s\t%s\n' % (title, '%d/%d' % (subdirectory, n_saved)))

                n_saved += 1
                if n_saved % max_num_files == 0:
                    subdirectory += 1
                if not os.path.exists('%s/%d/' % (directory, subdirectory)):
                    os.makedirs('%s/%d/' % (directory, subdirectory))
                    
                if debug and i >= 1000: 
                    break
    if verbose:
        sys.stdout.write('\rdone')
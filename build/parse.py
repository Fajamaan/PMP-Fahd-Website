import os

SL = r'C:\Users\Fajam\MyClaude\build\extract\ppt\slides'
OUTDIR = r'C:\Users\Fajam\MyClaude\build'

def texts_in(fragment):
    out = []
    i = 0
    while True:
        s = fragment.find('<a:t>', i)
        if s == -1:
            s2 = fragment.find('<a:t ', i)
            if s2 == -1:
                break
            gt = fragment.find('>', s2)
            e = fragment.find('</a:t>', gt)
            out.append(fragment[gt+1:e])
            i = e + 6
            continue
        e = fragment.find('</a:t>', s)
        out.append(fragment[s+5:e])
        i = e + 6
    return ''.join(out)

def paragraphs(shape):
    paras = []
    parts = shape.split('<a:p>')
    for p in parts[1:]:
        end = p.find('</a:p>')
        frag = p if end == -1 else p[:end]
        txt = texts_in(frag).strip()
        paras.append(txt)
    return paras

def is_arabic(s):
    for ch in s:
        if '؀' <= ch <= 'ۿ':
            return True
    return False

def unescape(s):
    return (s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
             .replace('&quot;', '"').replace('&apos;', "'"))

def parse_slide(num):
    path = os.path.join(SL, 'slide%d.xml' % num)
    xml = open(path, encoding='utf-8').read()
    if 'Try this' not in xml:
        return None
    shapes = xml.split('<p:sp>')
    en_paras = []
    ar_paras = []
    for sh in shapes[1:]:
        paras = [unescape(p) for p in paragraphs(sh) if p.strip()]
        if not paras:
            continue
        joined = ' '.join(paras)
        if joined.strip() == 'Try this':
            continue
        if is_arabic(joined):
            ar_paras = paras
        else:
            en_paras = [p for p in paras if p.strip() != 'Try this']
    return en_paras, ar_paras

def split_q_opts(paras):
    labels = ['A.', 'B.', 'C.', 'D.', 'E.']
    opt_idx = []
    for i, p in enumerate(paras):
        ps = p.strip()
        for L in labels:
            if ps.startswith(L):
                opt_idx.append(i)
                break
    if len(opt_idx) >= 3:
        first = opt_idx[0]
        q = ' '.join(x.strip() for x in paras[:first]).strip()
        opts = []
        for i in opt_idx:
            t = paras[i].strip()
            for L in labels:
                if t.startswith(L):
                    t = t[len(L):].strip()
                    break
            opts.append(t)
        return q, opts
    nonempty = [p.strip() for p in paras if p.strip()]
    if len(nonempty) >= 5:
        opts = nonempty[-4:]
        q = ' '.join(nonempty[:-4]).strip()
        return q, opts
    return ' '.join(nonempty), []

def split_ar(paras):
    nonempty = [p.strip() for p in paras if p.strip()]
    if len(nonempty) >= 5:
        q = ' '.join(nonempty[:-4]).strip()
        opts = nonempty[-4:]
        return q, opts
    if nonempty:
        return nonempty[0], nonempty[1:]
    return '', []

nums = []
for f in os.listdir(SL):
    if f.startswith('slide') and f.endswith('.xml'):
        try:
            n = int(f[5:-4])
        except ValueError:
            continue
        nums.append(n)
nums.sort()

records = []
for n in nums:
    r = parse_slide(n)
    if not r:
        continue
    en, ar = r
    q, opts = split_q_opts(en)
    aq, aopts = split_ar(ar)
    if len(opts) < 2:
        continue
    records.append({'slide': n, 'q': q, 'opts': opts, 'aq': aq, 'aopts': aopts})

with open(os.path.join(OUTDIR, 'questions_dump.txt'), 'w', encoding='utf-8') as f:
    for i, r in enumerate(records, 1):
        f.write('### Q%d (slide %d)\n' % (i, r['slide']))
        f.write('Q: %s\n' % r['q'])
        for j, o in enumerate(r['opts']):
            f.write('  %s) %s\n' % ('ABCDE'[j], o))
        f.write('\n')

print('questions:', len(records))

def jstr(s):
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    s = s.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return '"' + s + '"'

def jarr(lst):
    return '[' + ','.join(jstr(x) for x in lst) + ']'

with open(os.path.join(OUTDIR, 'questions_data.js'), 'w', encoding='utf-8') as f:
    f.write('const RAW_QUESTIONS = [\n')
    for r in records:
        f.write('{slide:%d,q:%s,opts:%s,aq:%s,aopts:%s},\n' % (
            r['slide'], jstr(r['q']), jarr(r['opts']), jstr(r['aq']), jarr(r['aopts'])))
    f.write('];\n')
print('done')

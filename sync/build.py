#!/usr/bin/env python3
"""Claude 아티팩트 원본을 수업페이지 파일로 옮긴다.

사용법:
  python3 sync/build.py [--main ../nohclass/index.html] nephron=/path/index.html diurnal=/path/index.html ...

- 원본 HTML은 그대로 두고 두 가지만 더한다: <html lang="ko">, 오른쪽 아래 '⌂ 처음으로' 버튼.
- 원본의 <title>을 수업페이지 첫 화면(와 --main 으로 준 메인페이지)의 카드 제목 <b data-sync="id">에 맞춘다.
- 바뀐 파일 목록을 출력한다. 바뀐 게 없으면 'no changes'.
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES = {s["id"]: s for s in json.loads((ROOT / "sync" / "sources.json").read_text())}
BTN = ('<a href="{back}" data-sync-home style="position:fixed;right:max(12px,env(safe-area-inset-right,0px));'
       'bottom:max(12px,env(safe-area-inset-bottom,0px));z-index:2147483000;font-family:Jua,\'Gowun Dodum\',sans-serif;'
       'font-size:14px;text-decoration:none;color:#2b2f55;background:#fff;border:2px solid #dde2f7;border-radius:999px;'
       'padding:4px 12px;box-shadow:0 4px 12px rgba(90,100,170,.18)">⌂ 처음으로</a>\n')

def build(src: str, back: str) -> str:
    out = re.sub(r"<html(\s[^>]*)?>", lambda m: m.group(0) if "lang=" in m.group(0) else m.group(0)[:-1].rstrip() + ' lang="ko">', src, count=1, flags=re.I)
    out = re.sub(r'<a [^>]*data-sync-home[^>]*>.*?</a>\n?', "", out, flags=re.S)  # 예전 버튼 지우기
    i = out.lower().rfind("</body>")
    if i < 0:
        i = out.lower().rfind("</html>")
    if i < 0:
        i = len(out)
    return out[:i] + BTN.format(back=back) + out[i:]

def set_card_title(page: pathlib.Path, sid: str, title: str) -> bool:
    if not page.exists():
        return False
    s = page.read_text()
    new = re.sub(r'(<b data-sync="%s">)(.*?)(</b>)' % re.escape(sid), lambda m: m.group(1) + html.escape(title, quote=False) + m.group(3), s)
    if new != s:
        page.write_text(new)
        return True
    return False

def main(argv):
    main_page = None
    pairs = []
    it = iter(argv)
    for a in it:
        if a == "--main":
            main_page = pathlib.Path(next(it))
        else:
            sid, _, path = a.partition("=")
            pairs.append((sid, pathlib.Path(path)))
    changed = []
    for sid, path in pairs:
        if sid not in SOURCES:
            sys.exit(f"unknown id: {sid}")
        src = path.read_text()
        target = ROOT / SOURCES[sid]["file"]
        out = build(src, SOURCES[sid]["back"])
        if not target.exists() or target.read_text() != out:
            target.write_text(out)
            changed.append(SOURCES[sid]["file"])
        m = re.search(r"<title>(.*?)</title>", src, re.S | re.I)
        if m:
            title = html.unescape(m.group(1)).strip()
            if set_card_title(ROOT / "index.html", sid, title):
                changed.append(f"index.html (카드 제목: {title})")
            if main_page and set_card_title(main_page, sid, title):
                changed.append(f"{main_page} (카드 제목: {title})")
    print("\n".join(changed) if changed else "no changes")

if __name__ == "__main__":
    main(sys.argv[1:])

from os import system
from save_url import __version__

def translate():
        #es
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o save_url/locale/save_url.pot save_url/*.py")
        system("msgmerge -N --no-wrap -U save_url/locale/es.po save_url/locale/save_url.pot")
        system("msgmerge -N --no-wrap -U save_url/locale/en.po save_url/locale/save_url.pot")
        system("msgfmt -cv -o save_url/locale/es/LC_MESSAGES/save_url.mo save_url/locale/es.po")
        system("msgfmt -cv -o save_url/locale/en/LC_MESSAGES/save_url.mo save_url/locale/en.po")

def release():
    print("""Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Cambiar la versión en pyproject.toml
  * Modificar el Changelog en README
  * poe translate
  * Update *.po files
  * poe translate
  * git commit -a -m 'save_url-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * poetry build
  * poetry publish --username --password  
  * Crea un nuevo ebuild de save_url Gentoo con la nueva versión
  * Subelo al repositorio del portage

""".format(__version__))


def monolith_ebuild():
    v="2.10.1"
    print(f"""Procedure to update monolith ebuild
    * emerge -v pycargoebuild
    * cd /tmp
    * git clone https://github.com/Y2Z/monolith
    * cd monolith
    * git checkout v{v}
    * pycargoebuild
    * mv monolith-{v}.ebuild /var/db/repos/myportage/www-apps/monolith/
    * Edit new ebuild adding in a new line of src_uri: https://github.com/Y2Z/monolith/archive/v{v}.tar.gz -> ${{P}}.tar.gz"
""")

# Maintainer: Cesar <yugurta@gmail.com>
pkgname=krunner-raycast-git
pkgver=1.0.0
pkgrel=1
pkgdesc="Raycast quick actions, dev utilities, bangs, and tool suites runner for KRunner on KDE Plasma 6"
arch=('any')
url="https://github.com/cesarconte/krunner-raycast"
license=('GPL-3.0-or-later')
depends=('python' 'python-dbus' 'python-gobject' 'wl-clipboard' 'libnotify')
optdepends=(
    'wireplumber: control de volumen y micrófono'
    'kocr: captura rápida de OCR en pantalla'
    'klivetext: detector interactivo de datos en pantalla'
    'kduck: atenuación de volumen multimedia inteligente'
    'kautomator: reglas de carpetas inteligentes'
)
provides=('krunner-raycast')
conflicts=('krunner-raycast')
source=("git+https://github.com/cesarconte/krunner-raycast.git")
sha256sums=('SKIP')

pkgver() {
    cd "${srcdir}/krunner-raycast"
    printf "1.0.0.r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd "${srcdir}/krunner-raycast"
    
    install -Dm755 bin/krunner-raycast "${pkgdir}/usr/bin/krunner-raycast"
    
    install -d "${pkgdir}/usr/share/krunner-raycast/src"
    cp -r src/* "${pkgdir}/usr/share/krunner-raycast/src/"
    
    install -Dm644 data/org.cesar.krunner_raycast.desktop "${pkgdir}/usr/share/krunner/dbusplugins/org.cesar.krunner_raycast.desktop"
    install -Dm644 data/org.cesar.KRunnerRaycast.service "${pkgdir}/usr/share/dbus-1/services/org.cesar.KRunnerRaycast.service"
    install -Dm644 data/krunner-raycast.service "${pkgdir}/usr/lib/systemd/user/krunner-raycast.service"
    install -Dm644 data/org.cesar.krunner_raycast.app.desktop "${pkgdir}/usr/share/applications/org.cesar.krunner_raycast.desktop"
    install -Dm644 README.md "${pkgdir}/usr/share/doc/krunner-raycast/README.md"
}

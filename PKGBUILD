# Maintainer: Your Name <your.email@example.com>

pkgname=TxtEd
pkgver=1.2
pkgrel=1
pkgdesc="A simple text editor using Python and PyQt6"
arch=('any')
url="https://github.com/l0vemimi/TxtEd"
license=('GPL')
depends=('python' 'python-pyqt6' 'python-pyqt6-webengine' 'python-pygments')
source=("$pkgname-$pkgver.tar.gz::https://github.com/l0vemimi/ArchPkg/raw/main/repo/x86_64/TxtEd-$pkgver.pkg.tar.zst")
#source=("$pkgname-$pkgver.tar.gz")
md5sums=('SKIP')

package() {
  cd "$srcdir/TxtEd"
  install -Dm755 txted-qt6.py "$pkgdir/usr/bin/txted"
  install -Dm644 txted-qt6.desktop "$pkgdir/usr/share/applications/txted-qt6.desktop"
  install -Dm644 img/txted.png "$pkgdir/usr/share/pixmaps/txted.png"
}
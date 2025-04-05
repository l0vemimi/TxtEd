# Maintainer: Your Name <your.email@example.com>

pkgname=txted
pkgver=1.0.0
pkgrel=1
pkgdesc="A simple text editor using Python and PyQt6"
arch=('any')
url="https://github.com/l0vemimi/TxtEd"
license=('GPL')
depends=('python' 'python-pyqt6' 'python-pyqt6-webengine' 'python-pygments')
source=("$pkgname-$pkgver.tar.gz::https://github.com/l0vemimi/ArchPkg/releases/download/v$pkgver/txted-$pkgver.tar.gz")

package() {
  cd "$srcdir/TxtEd-$pkgver"
  install -Dm755 txted-qt6.py "$pkgdir/usr/bin/txted"
  install -Dm644 txted-qt6.desktop "$pkgdir/usr/share/applications/txted.desktop"
  install -Dm644 txt-qt.png "$pkgdir/usr/share/pixmaps/txt-qt.png"
}
#!/bin/bash
# NetChat Sunucu Kurulum Scripti — Ubuntu 22.04 / 24.04
# Kullanım: sudo bash setup.sh

set -e

echo "==> Python 3.12 kontrol ediliyor..."
if ! python3 --version | grep -qE "3\.(1[0-9]|[2-9][0-9])"; then
    echo "==> Python 3.10+ bulunamadı, yükleniyor..."
    apt-get update -qq
    apt-get install -y software-properties-common
    add-apt-repository -y ppa:deadsnakes/ppa
    apt-get update -qq
    apt-get install -y python3.12 python3.12-venv
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
fi

echo "==> Python sürümü: $(python3 --version)"

echo "==> netchat kullanıcısı oluşturuluyor..."
id -u netchat &>/dev/null || useradd -r -s /bin/false netchat

echo "==> /opt/netchat dizini hazırlanıyor..."
mkdir -p /opt/netchat
cp -r "$(dirname "$(realpath "$0")")/.." /opt/netchat_tmp
cp -r /opt/netchat_tmp/. /opt/netchat/
rm -rf /opt/netchat_tmp
chown -R netchat:netchat /opt/netchat

echo "==> Güvenlik duvarı port 9000 açılıyor..."
if command -v ufw &>/dev/null; then
    ufw allow 9000/tcp
    echo "   ufw: port 9000 açıldı"
fi

echo "==> systemd servisi kuruluyor..."
cp /opt/netchat/deploy/netchat.service /etc/systemd/system/netchat.service
systemctl daemon-reload
systemctl enable netchat
systemctl restart netchat

echo ""
echo "========================================="
echo " NetChat başarıyla kuruldu ve çalışıyor!"
echo "========================================="
systemctl status netchat --no-pager
echo ""
echo " Sunucu IP'nizi öğrenmek için:"
echo "   curl -s ifconfig.me"
echo ""
echo " Log takibi için:"
echo "   journalctl -u netchat -f"
echo "========================================="

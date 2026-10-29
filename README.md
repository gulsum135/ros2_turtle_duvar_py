# turtle_duvar_py — Duvardan Kaçan Kaplumbağa

ROS 2 (Python / `rclpy`) ile yazılmış, `turtlesim` kaplumbağasının duvarlara
çarpmadan dolaşmasını sağlayan basit bir paket.

## Ne yapar?

| Görev | Uygulama |
|-------|----------|
| **Abone** | `/turtle1/pose` konusunu dinler, `x` ve `y` değerlerini alır |
| **Yayıncı** | `/turtle1/cmd_vel` ile kaplumbağayı ileri sürer |
| **Duvar kaçınma** | `x` veya `y` değeri `1.0`'dan küçük ya da `10.0`'dan büyükse kaplumbağa sahanın merkezine doğru dönerek yön değiştirir |
| **Log** | Konum, saniyede bir `get_logger().info()` ile yazdırılır |
| **Bonus** | Hız ve sınır değerleri ROS parametresidir |

## Paket yapısı

```
turtle_duvar_py/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/turtle_duvar_py
├── launch/duvar.launch.py
├── images/                     # ekran görüntüleri
└── turtle_duvar_py/
    ├── __init__.py
    └── duvar_kacan.py          # ana düğüm
```

## Gereksinimler

- ROS 2 (Humble)
- `turtlesim` paketi: `sudo apt install ros-$ROS_DISTRO-turtlesim`



## Çalıştırma

**Terminal 1** — simülatör:

```bash
ros2 launch turtle_duvar_py duvar.launch.py
```

Örnek log çıktısı:

```
[INFO] [duvar_kacan]: Konum: x=5.54, y=5.54, theta=0.00 | durum: ILERI
[INFO] [duvar_kacan]: Konum: x=7.04, y=5.54, theta=0.00 | durum: ILERI
[INFO] [duvar_kacan]: Konum: x=9.54, y=5.54, theta=0.00 | durum: ILERI
```

## Parametreler (Bonus)

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| `linear_speed` | `1.5` | İleri hız (m/s) |
| `angular_speed` | `2.0` | Dönüş hızı (rad/s) |
| `min_limit` | `1.0` | x ve y için alt sınır |
| `max_limit` | `10.0` | x ve y için üst sınır |
| `log_period` | `1.0` | Log periyodu (sn) |

Komut satırından:

```bash
ros2 run turtle_duvar_py duvar_kacan --ros-args \
  -p linear_speed:=2.5 -p angular_speed:=3.0 -p min_limit:=2.0 -p max_limit:=9.0
```

Launch ile:

```bash
ros2 launch turtle_duvar_py duvar.launch.py linear_speed:=2.5 min_limit:=2.0 max_limit:=9.0
```

Çalışırken değiştirme:

```bash
ros2 param set /duvar_kacan linear_speed 3.0
```

## Algoritma

1. `pose_callback` en son konumu saklar.
2. 10 Hz'lik kontrol döngüsü konumu sınırlarla karşılaştırır.
3. Sınırın **içindeyse** düz ileri gider (`linear.x = linear_speed`).
4. Sınırın **dışındaysa** önce yerinde döner (`angular.z = ±angular_speed`)
   ve yönü sahanın merkezine çevirir; yön doğru olunca ileri giderek
   sınırın içine geri döner.
5. Ayrı bir zamanlayıcı saniyede bir konumu loglar.


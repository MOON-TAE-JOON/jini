def create_choir_v3(filename="Choir.mid"):
    tempo = 60000000 // 180
    tpq = 480

    chords = [
        [74, 77, 81],
        [70, 74, 77],
        [72, 76, 79],
        [77, 81, 84],
        [81, 84, 88]
    ]

    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +
        (1).to_bytes(2, "big") +
        tpq.to_bytes(2, "big")
    )

    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Program change (Choir Aahs)
    track += b"\x00" + bytes([0xC0, 52])

    # 64 measures
    for i in range(64):
        chord = chords[i % 5]

        # Beat 1
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x90, note, 70])
        track += write_varlen(tpq)
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x80, note, 40])

        # Beat 2
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x90, note, 70])
        track += write_varlen(tpq)
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x80, note, 40])

        # Beat 3
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x90, note, 70])
        track += write_varlen(tpq)
        for note in chord:
            track += write_varlen(0)
            track += bytes([0x80, note, 40])

        # Beat 4 = rest
        track += write_varlen(tpq)

    # End track
    track += b"\x00\xFF\x2F\x00"

    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🎶 Choir.mid (v3) 생성 완료 – 모든 플레이어 호환")

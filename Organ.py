def write_varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)


def create_organ_v3(filename="Organ.mid"):
    tempo = 60000000 // 180
    tpq = 480

    chords = [
        [62, 65, 69],
        [58, 62, 65],
        [60, 64, 67],
        [65, 69, 72],
        [69, 72, 76]
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

    # Program change (Organ)
    track += b"\x00" + bytes([0xC0, 19])

    # 64 measures
    for i in range(64):
        chord = chords[i % 5]

        # 4 beats per bar → beat-by-beat sustain
        for _ in range(4):
            # note_on for chord
            for note in chord:
                track += write_varlen(0)
                track += bytes([0x90, note, 90])

            # sustain for 1 beat
            track += write_varlen(tpq)

            # note_off for chord
            for note in chord:
                track += write_varlen(0)
                track += bytes([0x80, note, 60])

    # End track
    track += b"\x00\xFF\x2F\x00"

    chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    with open(filename, "wb") as f:
        f.write(header + chunk)

    print("🎹 Organ.mid (v3) 생성 완료 – 모든 플레이어 호환")

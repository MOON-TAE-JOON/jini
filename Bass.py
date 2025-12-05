# ------------------------------------------------------------
# Bass.mid – 하드록 베이스 루트 톤 8분음표 패턴
# 외부 라이브러리 없이 순수 Python MIDI 생성
# ------------------------------------------------------------

def write_varlen(value):
    bytes_out = []
    bytes_out.append(value & 0x7F)
    value >>= 7
    while value:
        bytes_out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(bytes_out)

def create_midi_bass(filename="Bass.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    eighth = tpq // 2        # 8분음표
    velocity = 100

    # 베이스 루트 톤 (1옥타브 낮춤)
    bass_roots = {
        "Dm": 38,  # D1
        "Bb": 34,  # Bb0
        "C": 36,   # C1
        "F": 41,   # F1
        "A": 45    # A1
    }

    progression = ["Dm", "Bb", "C", "F", "A"]

    # --- Header ---
    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +
        (1).to_bytes(2, "big") +
        tpq.to_bytes(2, "big")
    )

    # --- Track ---
    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Program change → Electric Bass (Finger, 34)
    track += b"\x00" + bytes([0xC0, 34])

    # 64마디 * 4박자 * 2 (8분음표) = 512 note events
    for i in range(64):
        root = bass_roots[progression[i % len(progression)]]

        for step in range(8):  # 한 마디 8개 8분음표
            # note_on
            track += write_varlen(0)
            track += bytes([0x90, root, velocity])

            # note_off after 8th note
            track += write_varlen(eighth)
            track += bytes([0x80, root, 64])

    # End track
    track += b"\x00\xFF\x2F\x00"

    # Build track chunk
    track_chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    # Save
    with open(filename, "wb") as f:
        f.write(header + track_chunk)

    print("🎸 Bass.mid 생성 완료")

# Run
create_midi_bass()

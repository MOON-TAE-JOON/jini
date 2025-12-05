# ------------------------------------------------------------
# Guitar_R.mid – 하드록 리듬 기타(우) 더블 트래킹
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

def create_midi_guitar_R(filename="Guitar_R.mid"):
    tempo = 60000000 // 180  # BPM 180
    tpq = 480
    duration = tpq           # 1 beat
    delay = 5                # 더블트래킹용 5 tick 딜레이

    # Guitar R 파워코드 root-notes
    power_roots = {
        "Dm": 50,   # D2
        "Bb": 46,   # Bb1
        "C": 48,    # C2
        "F": 53,    # F2
        "A": 57     # A2
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

    # Program change: Distortion Guitar (30)
    track += b"\x00" + bytes([0xC0, 30])

    # Note events
    for i in range(64):
        root = power_roots[progression[i % len(progression)]]

        # note_on (약간 딜레이)
        track += write_varlen(delay)
        track += bytes([0x90, root, 96])   # velocity 약간 낮게

        # note_off
        track += write_varlen(duration)
        track += bytes([0x80, root, 64])

    # End track
    track += b"\x00\xFF\x2F\x00"

    # Wrap track chunk
    track_chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    # Save file
    with open(filename, "wb") as f:
        f.write(header + track_chunk)

    print("🎸 Guitar_R.mid 생성 완료")

# Run
create_midi_guitar_R()

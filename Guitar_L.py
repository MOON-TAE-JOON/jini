# ------------------------------------------------------------
# Guitar_L.mid – 하드록 리듬 기타(좌) 파워코드 패턴
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

def create_midi_guitar_L(filename="Guitar_L.mid"):
    # tempo 180bpm → μs per quarter
    tempo = 60000000 // 180
    tpq = 480
    duration = tpq  # 1박자

    # 파워코드 root-note만 사용 (L 채널)
    power_roots = {
        "Dm": 50,   # D2
        "Bb": 46,   # Bb1
        "C": 48,    # C2
        "F": 53,    # F2
        "A": 57     # A2
    }

    progression = ["Dm", "Bb", "C", "F", "A"]

    # --- MIDI header ---
    header = (
        b"MThd" +
        (6).to_bytes(4, "big") +
        (0).to_bytes(2, "big") +      # Format 0
        (1).to_bytes(2, "big") +      # Tracks = 1
        tpq.to_bytes(2, "big")
    )

    # --- Track ---
    track = bytearray()

    # Tempo
    track += b"\x00\xFF\x51\x03" + tempo.to_bytes(3, "big")

    # Program change → Distortion Guitar (Program 30)
    track += b"\x00"                  # delta time
    track += bytes([0xC0, 30])        # Program Change

    # Note events
    for i in range(64):
        root = power_roots[progression[i % len(progression)]]

        # note_on
        track += write_varlen(0)
        track += bytes([0x90, root, 100])

        # note_off
        track += write_varlen(duration)
        track += bytes([0x80, root, 64])

    track += b"\x00\xFF\x2F\x00"  # End track

    # Track chunk
    track_chunk = b"MTrk" + len(track).to_bytes(4, "big") + track

    # Save
    with open(filename, "wb") as f:
        f.write(header + track_chunk)

    print("🎸 Guitar_L.mid 생성 완료")

# Run
create_midi_guitar_L()

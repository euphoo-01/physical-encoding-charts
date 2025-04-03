import matplotlib.pyplot as plt

def nrz_encoding(bits):
    return [1 if bit == '1' else -1 for bit in bits]

def nrzi_encoding(bits):
    signal = [1]
    for bit in bits:
        if bit == '1':
            signal.append(-signal[-1])
        else:
            signal.append(signal[-1])
    return signal[1:]

def ami_encoding(bits):
    signal = []
    polarity = 1
    for bit in bits:
        if bit == '1':
            signal.append(polarity)
            polarity *= -1
        else:
            signal.append(0)
    return signal

def bipolar_encoding(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal.extend([0, 1])
        else:
            signal.extend([0, -1])
    return signal

def manchester_encoding(bits):
    signal = []
    for bit in bits:
        if bit == '1':
            signal.extend([1, -1])
        else:
            signal.extend([-1, 1])
    return signal

def two_b_one_q_encoding(bits):
    mapping = {'00': 3, '01': 1, '10': -1, '11': -3}
    quads = [bits[i:i+2] for i in range(0, len(bits), 2)]
    return [mapping[quad] for quad in quads]

def hdb3_encoding(bits):
    signal = []
    polarity = 1
    zero_count = 0
    b_count = 0
    
    for bit in bits:
        if bit == '1':
            signal.append(polarity)
            polarity *= -1
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 4:
                signal = signal[:-3]
                
                if b_count % 2 == 0:
                    last_polarity = -polarity
                    signal.extend([0, 0, 0, last_polarity])
                else:
                    signal.extend([0, 0, 0, polarity])
                    polarity *= -1
                
                b_count += 1
                zero_count = 0
            else:
                signal.append(0)
    return signal

def b8zs_encoding(bits):
    signal = []
    polarity = 1
    zero_count = 0
    
    for bit in bits:
        if bit == '1':
            signal.append(polarity)
            polarity *= -1
            zero_count = 0
        else:
            zero_count += 1
            if zero_count == 8:
                signal = signal[:-7]
                
                if polarity == 1:
                    signal.extend([0, 0, 0, 0, -1, 1, 0, -1, 1])
                else:
                    signal.extend([0, 0, 0, 0, 1, -1, 0, 1, -1])
                
                zero_count = 0
            else:
                signal.append(0)
    
    return signal

def plot_signal(ax, x, y, title, yticks, xlim_extra=1.5, show_bits=True, bits=None):
    x_extended = list(x) + [max(x) + 1]
    y_extended = list(y) + [y[-1]]
    
    ax.step(x_extended, y_extended, where='post', linestyle='-', color='b')
    ax.set_title(title, fontsize=14)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_yticks(yticks)
    ax.set_xticks(x)
    ax.set_xlim(min(x) - xlim_extra, max(x_extended) + xlim_extra)
    ax.set_ylim(min(yticks) - 0.5, max(yticks) + 0.5)
    ax.tick_params(axis='x', labelbottom=False)
    
    for pos in x_extended:
        ax.axvline(pos, color='gray', linestyle='--', linewidth=0.5)
    
    if show_bits and bits:
        text_positions = []
        
        if title == "2B1Q":
            for i in range(len(quads)):
                text_positions.append((x[i] + x_extended[i+1]) / 2)
        elif title in ["Биполярный импульсный код", "Манчестерский код"]:
            for i in range(len(bits)):
                idx = i * 2
                if idx < len(x):
                    next_idx = (i + 1) * 2
                    if next_idx < len(x_extended):
                        text_positions.append((x[idx] + x_extended[next_idx]) / 2)
                    else:
                        text_positions.append((x[idx] + x_extended[-1]) / 2)
        else:
            for i in range(len(bits)):
                if i < len(x):
                    text_positions.append((x[i] + x_extended[i+1]) / 2)
        
        text_positions = text_positions[:len(bits)]
        
        for pos, bit in zip(text_positions, bits):
            ax.text(pos, max(yticks) + 0.3, bit, ha='center', fontsize=10)


print("Введите бинарную последовательность:")
binary_input = input()

x_nrz = list(range(1, len(binary_input) + 1))
nrz_signal = nrz_encoding(binary_input)

x_nrzi = list(range(1, len(binary_input) + 1))
nrzi_signal = nrzi_encoding(binary_input)

x_ami = list(range(1, len(binary_input) + 1))
ami_signal = ami_encoding(binary_input)

x_bipolar = []
for i in range(len(binary_input)):
    x_bipolar.extend([i*2 + 1, i*2 + 2])
bipolar_signal = bipolar_encoding(binary_input)

x_manchester = []
for i in range(len(binary_input)):
    x_manchester.extend([i*2 + 1, i*2 + 2])
manchester_signal = manchester_encoding(binary_input)

binary_input_2b1q = binary_input
if len(binary_input) % 2 != 0:
    binary_input_2b1q += '0'
quads = [binary_input_2b1q[i:i+2] for i in range(0, len(binary_input_2b1q), 2)]
x_2b1q = list(range(1, len(quads) + 1))
two_b_one_q_signal = two_b_one_q_encoding(binary_input_2b1q)

hdb3_signal = hdb3_encoding(binary_input)
x_hdb3 = list(range(1, len(hdb3_signal) + 1))

b8zs_signal = b8zs_encoding(binary_input)
x_b8zs = list(range(1, len(b8zs_signal) + 1))

plt.figure(figsize=(20, 14))

ax1 = plt.subplot(3, 3, 1)
plot_signal(ax1, x_nrz, nrz_signal, "NRZ", [-1, 1], show_bits=True, bits=binary_input)

ax2 = plt.subplot(3, 3, 2)
plot_signal(ax2, x_nrzi, nrzi_signal, "NRZI", [-1, 1], show_bits=True, bits=binary_input)

ax3 = plt.subplot(3, 3, 3)
plot_signal(ax3, x_ami, ami_signal, "AMI", [-1, 0, 1], show_bits=True, bits=binary_input)

ax4 = plt.subplot(3, 3, 4)
plot_signal(ax4, x_bipolar, bipolar_signal, "Биполярный импульсный код", [-1, 0, 1], show_bits=True, bits=binary_input)

ax5 = plt.subplot(3, 3, 5)
plot_signal(ax5, x_manchester, manchester_signal, "Манчестерский код", [-1, 1], show_bits=True, bits=binary_input)

ax6 = plt.subplot(3, 3, 6)
plot_signal(ax6, x_2b1q, two_b_one_q_signal, "2B1Q", [-3, -1, 1, 3], show_bits=True, bits=quads)

ax7 = plt.subplot(3, 3, 7)
plot_signal(ax7, x_hdb3, hdb3_signal, "HDB3", [-1, 0, 1], show_bits=True, bits=binary_input)

ax8 = plt.subplot(3, 3, 8)
plot_signal(ax8, x_b8zs, b8zs_signal, "B8ZS", [-1, 0, 1], show_bits=True, bits=binary_input)

plt.tight_layout()
plt.show()
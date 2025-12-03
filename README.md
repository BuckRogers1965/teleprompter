# Python Teleprompter

A precise, time-based teleprompter application built with Python and Pygame. Unlike standard scrolling text, this tool calculates scrolling speed based on a specific **target duration**, ensuring your presentation finishes exactly on time.

## The Science: Why use a Teleprompter?

While speed-reading tools (RSVP) are designed for rapid information *input*, teleprompters are designed for high-quality information *output*.

### 1. The Parallax Effect and Eye Contact
The primary "science" of a teleprompter setup involves the **Beam Splitter Glass**. By placing a monitor flat on the ground and angling a semi-transparent mirror at 45 degrees, the text is reflected in front of the camera lens.
*   **Without a prompter:** The speaker looks down at notes or off to the side, breaking the connection with the audience.
*   **With a prompter:** The speaker looks directly into the lens (and the viewer's eyes) while reading. This significantly increases perceived authority, trustworthiness, and engagement.

### 2. Cognitive Offloading
Speaking from memory requires significant cognitive resources. You are simultaneously retrieving information, structuring sentences, and managing body language.
*   **Cognitive Load Theory:** A teleprompter "offloads" the memory and structure tasks. This frees up the speaker's mental processing power to focus entirely on **prosody** (tone, rhythm, and emotion) and non-verbal communication.

### 3. Temporal Constraints
In broadcasting and professional speaking, time is currency. This tool utilizes a specific algorithm that takes the length of your text and your desired time limit (e.g., 60 seconds) to calculate the exact pixel-per-second scroll rate required. It ensures you never run long or short.

## Features

*   **Time-Based Scrolling:** Instead of setting an arbitrary speed (1x, 2x), you input the *Total Duration* (in seconds). The software mathematically calculates the scroll speed to ensure you finish exactly on time.
*   **Mirror Mode:** Includes a `--mirror` argument to horizontally flip the text, making it compatible with physical teleprompter glass/beam splitters.
*   **Smart Period Pausing:** The scroller automatically detects periods (`.`) and pauses momentarily. This mimics natural speech patterns, allowing the speaker to breathe and giving the audience time to digest the sentence.
*   **Focus Markers:** Red indicators on the side of the screen help keep your eyes fixed on the correct reading line to minimize vertical eye movement.

## Installation

This tool requires Python and Pygame.

```bash
pip install pygame
```

## Usage

Run the script from the command line by providing the text file and the desired duration in seconds.

### Basic Usage
Read `speech.txt` and ensure it takes exactly 2 minutes (120 seconds):

```bash
python teleprompter.py speech.txt 120
```

### Mirror Mode (For Beam Splitters)
If you are using a physical teleprompter glass, the text needs to be reversed on the monitor so it appears correct in the reflection.

```bash
python teleprompter.py speech.txt 120 --mirror
```

## Controls

| Key | Action |
| :--- | :--- |
| **SPACE** | Start / Pause scrolling |
| **ESC** | Quit application |

## Configuration

You can tweak the visual settings by editing the variables at the top of `teleprompter.py`:

*   `PAUSE_DURATION`: How long (in seconds) the text stops at a period.
*   `FONT_SIZE`: Adjust text readability.
*   `FOCUS_LINE_COLOR`: Change the color of the reading guide.
*   `SCREEN_WIDTH` / `SCREEN_HEIGHT`: Adjust for your monitor resolution.

```python
# Example Configuration in teleprompter.py
PAUSE_DURATION = 0.8   
FONT_SIZE = 60
FONT_COLOR = (255, 255, 255) 
BG_COLOR = (0, 0, 0)
```

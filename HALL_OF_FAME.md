# 🏆 Hall of Fame

Congratulations to everyone who solved the Brainfuck MD5 Collision Challenge!

## 🥇 Leaderboard

Rankings based on **total file size** (file1 + file2). Smaller is better!

| Rank | Name | Date | File 1 | File 2 | Total | Link |
|------|------|------|--------|--------|-------|------|
| - | *Awaiting first submission* | - | - | - | - | - |

*Be the first to submit your solution!*

---

## 📝 Submissions

*No submissions yet. Be the first!*

---

## 🎯 How to Submit Your Solution

### Step 1: Solve the Challenge
Visit [collision.hacknroll.academy](https://collision.hacknroll.academy/) and create two Brainfuck programs that:
- File 1 outputs "Rock N Roll"
- File 2 outputs "Hack N Roll"  
- Both have identical MD5 hashes

### Step 2: Encode Your Files to Base64

**Linux/Mac:**
```bash
base64 -w 0 rock.bf > rock_b64.txt
base64 -w 0 hack.bf > hack_b64.txt
```

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("rock.bf")) | Out-File -Encoding ASCII rock_b64.txt
[Convert]::ToBase64String([IO.File]::ReadAllBytes("hack.bf")) | Out-File -Encoding ASCII hack_b64.txt
```

**Python (cross-platform):**
```python
import base64

with open('rock.bf', 'rb') as f:
    print(base64.b64encode(f.read()).decode())

with open('hack.bf', 'rb') as f:
    print(base64.b64encode(f.read()).decode())
```

### Step 3: Fork and Edit This File

1. Fork this repository on GitHub
2. Edit `HALL_OF_FAME.md`
3. Add your entry using the template below
4. Create a Pull Request with title: `Hall of Fame: [Your Name]`

### 📝 Submission Template

Copy this template and fill in your details:

````markdown
### [Your Name]
**Date:** [Month Day, Year]  
**Total Size:** XXX bytes (XXX + XXX)  
**MD5 Hash:** `[first 12 characters]...`

<details>
<summary>📦 View Files (Base64)</summary>

**rock.bf (XXX bytes):**
```
[paste base64 content - single line, no breaks]
```

**hack.bf (XXX bytes):**
```
[paste base64 content - single line, no breaks]
```

</details>

✅ **Verified by:** [Leave empty - maintainer will fill this]
````

### Step 4: Submit Pull Request

- **Title:** `Hall of Fame: [Your Name]`
- **Label:** Add `hall-of-fame` label
- **Description:** Brief note about your solution (optional)

We'll verify your submission and merge it! 🎉

---

## 📏 Submission Rules

1. ✅ File 1 must output exactly "Rock N Roll"
2. ✅ File 2 must output exactly "Hack N Roll"
3. ✅ Both files must have identical MD5 hashes
4. ✅ Files must be valid Brainfuck code
5. ✅ Base64 must be single line (no line breaks)
6. ✅ One submission per person (you can resubmit to improve)
7. ✅ Submissions will be manually verified before merging

---

## 🎖️ Special Achievements

Will be awarded as submissions come in:

- **🏅 Size Champion:** Smallest total submission
- **🎯 First Blood:** First person to solve the challenge
- **⚡ Speed Runner:** Fastest submission after launch
- **🔥 Most Creative:** Most elegant or creative approach
- **🌟 Community Hero:** Most helpful in discussions

---

## 📊 Statistics

Will be updated as submissions arrive:

- **Total Solvers:** 0
- **Average Size:** N/A
- **Smallest Solution:** N/A
- **Record Holder:** N/A

---

## 🤝 For Maintainers

### Verification Process

1. **Extract files from PR:**
   ```bash
   echo "[base64 from PR]" | base64 -d > rock.bf
   echo "[base64 from PR]" | base64 -d > hack.bf
   ```

2. **Run verification:**
   ```bash
   python scripts/verify_submission.py rock.bf hack.bf
   ```

3. **If valid:**
   - Add "✅ Verified by: @[your-username] on [date]"
   - Update leaderboard ranking
   - Update statistics
   - Merge PR
   - Comment: "🎉 Welcome to the Hall of Fame!"

4. **If invalid:**
   - Comment explaining the issue
   - Request corrections
   - Close if spam

---

## 💡 Tips for Solvers

- Smaller files rank higher!
- Study MD5 collision techniques
- Use tools like HashClash or FastColl
- Check the [SOLUTION.md](SOLUTION.md) for hints (spoilers!)
- Valid Brainfuck commands: `><+-.,[]`
- All other characters are comments (use wisely!)

---

## 🔗 Resources

- **Challenge:** [collision.hacknroll.academy](https://collision.hacknroll.academy/)
- **Repository:** [github.com/maycon/bf-md5-collision](https://github.com/maycon/bf-md5-collision)
- **Brainfuck Wiki:** [wikipedia.org/wiki/Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)
- **MD5 Collisions:** [wikipedia.org/wiki/MD5#Collision_vulnerabilities](https://en.wikipedia.org/wiki/MD5#Collision_vulnerabilities)

---

*Want your name here? [Submit your solution!](#how-to-submit-your-solution)* 🚀
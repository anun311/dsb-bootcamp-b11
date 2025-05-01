play_pyc <- function() {
  actions <- c('Rock', 'Paper', 'Scissors', 'Exit') # กำหนดเงื่อนไขก่อน
  win <- 0; loss <- 0; tie <-0 # ตั้งค่าแต้มที่ได้ + รัน fn ใหม่ ให้ reset เป็น 0 
  
  while (TRUE) {
    player_move <- as.numeric(readline("Your move: [1] Rock, [2] Paper, [3] Scissors, [9] Exit: "))
    
    if (player_move == 9) {
      # บอก บ๊าย บาย พร้อมบอกคะแนน และจำนวนรอบการเล่น
      cat("Bye bye 👋 :)\nYou play:", (win+loss+tie), "Rounds \n" )
      cat('WIN:', win, ' LOSS:', loss, ' TIE:', tie)
      break
    }
    
    player_move <- actions[player_move] # subset ไปหาความหมายใน actions ใช้ if ใน loop ต่อไป
    computer_move <- actions[sample(1:3, 1)] # ให้คอม sample มา 1 ค่า
    
    # if loop เฉพาะ tie กับ loss นอกนั้น win
    if(player_move == computer_move) {
      cat('This round : Tie😁 \n')
      tie <- tie + 1
    } else if (player_move == 'Rock' & computer_move == 'Paper') {
      cat('This round : Loss😭 \n')
      loss <- loss + 1
    } else if (player_move == 'Paper' & computer_move == 'Scissors') {
      cat('This round : Loss😭 \n')
      loss <- loss + 1
    } else if (player_move == 'Scissors' & computer_move == 'Rock') {
      cat('This round : Loss😭 \n')
      loss <- loss + 1
    } else {
      cat('This round : Win😎 \n')
      win <- win + 1
    }
    
    # บอกคะแนนที่ได้แต่ละรอบ
    cat("😍 Player Move:", player_move, '\n')
    cat("🕹 Computer Move:", computer_move, '\n')
    cat('WIN:', win, ' LOSS:', loss, ' TIE:', tie)
  }
}

# เรียก fn เพื่อเริ่มเล่น
play_pyc()

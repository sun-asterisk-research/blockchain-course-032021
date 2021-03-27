# Nonce
* là một số ngẫu nhiên có độ dài 32bit nằm trong blockheader
* Khi thực hiện hash sha256 với các thành phần khác trong blockheader(merke Root hash, timestamp, hash của các block
trước), nếu hash sinh ra nhỏ hơn hash mục tiêu(difficulty) thì minner có được dồng thuận và sở hữu block đó
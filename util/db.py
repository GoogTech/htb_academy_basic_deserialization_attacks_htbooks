# HTBooks GmbH & Co. KG
# 10.10.2022

import sqlite3
from . import config

# Data scraped from: https://www.topshelfcomix.com/catalog/isbn-list [Accessed on 10.10.2022]
# var items = document.getElementsByClassName("isbn-item"); var str = ""; for (var i = 0; i < items.length; i++) { str += "(\"" + items[i].children[2].innerText + "\", \"" + items[i].children[0].innerText + "\", " + (Math.floor(Math.random() * (3 - 1) ) + 1) + "),\n"; } console.log(str);

books = [
    ("Animal Stories, $19.99", "978-1-60309-502-0", 2),
    ("Cosmoknights (Book One), $19.99", "978-1-60309-454-2", 2),
    ("The Delicacy, $24.99", "978-1-60309-492-4", 2),
    ("Doughnuts and Doom, $14.99", "978-1-60309-513-6", 1),
    ("Dragon Puncher (Book 3): Dragon Puncher Punches Back, $9.99", "978-1-60309-514-3", 2),
    ("Essex County, $29.95", "978-1-60309-038-4", 2),
    ("Free Pass, $19.99", "978-1-60309-505-1", 2),
    ("From Hell: Master Edition #03 (of 10), $7.99", "UPC 827714016215 00311", 2),
    ("From Hell: Master Edition #05 (of 10), $7.99", "UPC 827714016215 00511", 2),
    ("From Hell: Master Edition #07 (of 10), $7.99", "UPC 827714016215 00711", 1),
    ("From Hell: Master Edition #08 (of 10), $7.99", "UPC 827714016215 00811", 1),
    ("From Hell: Master Edition #09 (of 10), $7.99", "UPC 827714016215 00911", 1),
    ("From Hell: Master Edition #10 (of 10), $7.99", "UPC 827714016215 01011", 1),
    ("From Hell: Master Edition -- HARDCOVER , $49.99", "978-1-60309-469-6", 2),
    ("The Fun Family, $24.99", "978-1-60309-344-6", 2),
    ("Glork Patrol (Book Two): Glork Patrol Takes a Bath, $9.99", "978-1-60309-504-4", 1),
    ("Hey, Mister (Vol 1): After School Special by Sickman-Garner, $7.95", "978-1-891830-02-0", 1),
    ("Hey, Mister (Vol 3): The Fall Collection by S-Garner, $12.95", "978-1-891830-25-9", 1),
    ("Hey, Mister: Come Hell or Highwater Pants, $14.95", "978-1-60309-030-8", 1),
    ("Home Time: Under the River, $24.99", "978-1-60309-412-2", 1),
    ("Incredible Change-Bots One, $14.95", "978-1-891830-91-4", 1),
    ("Incredible Change-Bots Two, $14.95", "978-1-60309-067-4", 2),
    ("Johnny Boo (Book 2): Twinkle Power, $9.95", "978-1-60309-015-5", 2),
    ("Johnny Boo (Book 3): Happy Apples, $9.95", "978-1-60309-041-4", 1),
    ("Johnny Boo (Book 5): Does Something!, $9.95", "978-1-60309-084-1", 2),
    ("Johnny Boo (Book 6): Zooms to the Moon!, $9.95", "9781603093491", 1),
    ("Johnny Boo (Book 7): Goes Like This!, $9.99", "978-1-60309-384-2", 2),
    ("Johnny Boo (Book 13): Johnny Boo Goes to School, $9.99", "978-1-60309-503-7", 2),
    ("Johnny Boo Meets Dragon Puncher!, $9.99", "9781603093682", 1),
    ("Johnny Boo's Big Boo Box (Slipcase Set of Books 1-5) All ages (4-8+), $39.99", "978-1-60309-385-9", 1),
    ("Junkwraith, $24.99", "978-1-60309-500-6", 2),
    ("Kodi, $14.99", "978-1-60309-467-2", 2),
    ("The League of Extraordinary Gentlemen (Vol III): Century - HARDCOVER, $29.95", "978-1-60309-329-3", 1),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest #2 (of 6), $4.99", "UPC 827714014280 00211", 2),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest #3 (of 6), $4.99", "UPC 827714014280 00311", 2),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest #4 (of 6), $4.99", "UPC 827714014280 00411", 1),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest #5 (of 6), $4.99", "UPC 827714014280 00511", 1),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest #6 (of 6), $4.99", "UPC 827714014280 00611", 2),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest (TPB), $19.99", "978-1-60309-496-2", 1),
    ("The League of Extraordinary Gentlemen (Vol IV): The Tempest -- HARDCOVER, $29.99", "978-1-60309-456-6", 1),
    ("Lost Girls (Expanded Edition), $49.99", "978-1-60309-436-8", 1),
    ("Loved and Lost: A Relationship Trilogy, $29.99", "978-1-60309-506-8", 2),
    ("March (Trilogy Slipcase Set), $49.99", "978-1-60309-395-8", 1),
    ("March: Book One, $14.95", "978-1-60309-300-2", 2),
    ("March: Book Three, $19.99", "978-1-60309-402-3", 1),
    ("March: Book Three -- HARDCOVER, $29.99", "978-1-60309-396-5", 2),
    ("Monster on the Hill (Expanded Edition), $19.95", "978-1-60309-491-7", 2),
    ("Nemo: Heart of Ice, $14.95", "978-1-60309-274-6", 2),
    ("Nemo: River of Ghosts, $14.95", "978-1-60309-355-2", 2),
    ("Nemo: The Roses of Berlin, $14.95", "978-1-60309-320-0", 2),
    ("Onion Skin, $14.99", "978-1-60309-489-4", 2),
    ("Order of the Night Jay (Book One): The Forest Beckons, $14.99", "978-1-60309-510-5", 1),
    ("Our Expanding Universe, $19.99", "978-1-60309-377-4", 2),
    ("Parenthesis, $19.99", "978-1-60309-481-8", 2),
    ("Pinocchio, Vampire Slayer (Vol. 2): The Great Puppet Theater, TBD", "9781603093255", 1),
    ("Radical: My Year with a Socialist Senator, $24.99", "978-1-60309-512-9", 1),
    ("Red Panda & Moon Bear (Book Two): The Curse of the Evil Eye, $14.99", "978-1-60309-501-3", 1),
    ("Return of the Dapper Men (Deluxe Edition), $34.99", "978-1-60309-413-9", 2),
    ("Rivers, $19.99", "978-1-60309-490-0", 2),
    ("Secret Passages, $19.99", "978-1-60309-499-3", 2),
    ("Super Tokyoland, $24.99", "978-1-60309-418-4", 2),
    ("Superf*ckers Forever, $17.99", "9781684050895", 2),
    ("Surfside Girls (Book One): The Secret of Danger Point, $14.99", "978-1-60309-411-5", 2),
    ("Surfside Girls (Book Two): The Mystery at the Old Rancho, $14.99", "978-1-60309-447-4", 1),
    ("The Science of Surfing: A Surfside Girls Guide to the Ocean , $9.99", "978-1-60309-494-8", 2),
    ("The Surrogates Owner's Manual, $39.95", "978-1-60309-045-2", 1),
    ("The Surrogates: Case Files #1, TBD", "978-1-60309-258-6", 2),
    ("They Called Us Enemy, $19.99", "978-1-60309-450-4", 2),
    ("They Called Us Enemy: Expanded Hardcover Edition, $29.99", "978-1-60309-470-2", 2),
    ("Tonoharu (Part Two), $19.95", "978-0-9801023-3-8", 1),
    ("Tonoharu (Part Three), $24.95", "978-0-9801023-1-4", 1),
    ("The Underwater Welder - HARDCOVER, $29.99", "978-1-60309-392-7", 2),
    ("The Underwater Welder - SIGNED & NUMBERED HARDCOVER, $49.99", "978-1-60309-398-9", 1),
    ("Voice of the Fire by Alan Moore with José Villarrubia, $14.95", "978-1-60309-035-3", 1),
    ("Voice of the Fire (25th Anniversary Edition), $14.99", "978-1-60309-507-5", 1),
    ("Ashes, $19.99", "978-1-60309-517-4", 1),
    ("Cosmic Cadets (Book One): Contact!, $14.99", "978-1-60309-520-4", 2),
    ("Cosmoknights (Book Two), $24.99", "978-1-60309-511-2", 1),
    ("Edmund White's A Boy's Own Story: The Graphic Novel, $29.99", "978-1-60309-508-2", 2),
    ("F.A.R.M. System, $19.99", "978-1-60309-515-0", 1),
    ("Glork Patrol (Book Three): Glork Patrol and the Magic Robot, $9.99", "978-1-60309-521-1", 2),
    ("Shelley Frankenstein! (Book One): CowPiggy, $14.99", "978-1-60309-522-8", 2),
    ("Skull Cat (Book One): Skull Cat and the Curious Castle, $14.99", "978-1-60309-519-8", 2),
    ("Super Trash Clash, $14.99", "978-1-60309-516-7", 1)
]

con = sqlite3.connect(config.DB_NAME)
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("DROP TABLE IF EXISTS books")
cur.execute("CREATE TABLE users (username, password, role)")
cur.execute("INSERT INTO users VALUES ('admin', '$2a$12$CI5xUwphLIAMe4y7MKzR8e6jqAUGSq1hWbf66/vQLH0WxdmnhY1qC', 'admin')")
# franz.mueller:bierislekker
# Ref: https://academy.hackthebox.com/module/169/section/1647
cur.execute("INSERT INTO users VALUES ('franz.mueller', '$2a$12$BhhOO522iyolFadMQW/T0eMhzbGH67zqWShPwYWZKkshuacSPqZKS', 'user')")
cur.execute("CREATE TABLE books (name, isbn, status)")
cur.executemany("INSERT INTO books VALUES (?, ?, ?)", books)
con.commit()
con.close()

def getBooks():
    con = sqlite3.connect(config.DB_NAME)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM books")
    books = res.fetchall()
    con.close()
    return books
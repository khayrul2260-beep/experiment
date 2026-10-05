"""
NAFI
===========================================================
Bangladesh District → Area / Upazila Location Data

Official administrative source:
- 64 Districts
- 500 Upazilas
- Updated for 2026

Dhaka additionally contains common city delivery areas
for better e-commerce checkout usability.
===========================================================
"""


# =========================================================
# OFFICIAL DISTRICT → UPAZILA DATA
# =========================================================

OFFICIAL_UPAZILAS = {

    # =====================================================
    # DHAKA DIVISION
    # =====================================================

    "Dhaka": [
        "Dhamrai",
        "Dohar",
        "Keraniganj",
        "Nawabganj",
        "Savar",
    ],

    "Faridpur": [
        "Alfadanga",
        "Bhanga",
        "Boalmari",
        "Charbhadrasan",
        "Faridpur Sadar",
        "Madhukhali",
        "Nagarkanda",
        "Sadarpur",
        "Saltha",
    ],

    "Gazipur": [
        "Gazipur Sadar",
        "Kaliakair",
        "Kaliganj",
        "Kapasia",
        "Sreepur",
    ],

    "Gopalganj": [
        "Gopalganj Sadar",
        "Kashiani",
        "Kotalipara",
        "Muksudpur",
        "Tungipara",
    ],

    "Kishoreganj": [
        "Austagram",
        "Bajitpur",
        "Bhairab",
        "Hossainpur",
        "Itna",
        "Karimganj",
        "Katiadi",
        "Kishoreganj Sadar",
        "Kuliarchar",
        "Mithamain",
        "Nikli",
        "Pakundia",
        "Tarail",
    ],

    "Madaripur": [
        "Kalkini",
        "Madaripur Sadar",
        "Rajoir",
        "Shibchar",
        "Dasar",
    ],

    "Manikganj": [
        "Daulatpur",
        "Ghior",
        "Harirampur",
        "Manikganj Sadar",
        "Saturia",
        "Shibalaya",
        "Singair",
    ],

    "Munshiganj": [
        "Gazaria",
        "Lohajang",
        "Munshiganj Sadar",
        "Sirajdikhan",
        "Sreenagar",
        "Tongibari",
    ],

    "Narayanganj": [
        "Araihazar",
        "Sonargaon",
        "Narayanganj Sadar",
        "Rupganj",
        "Bandar",
    ],

    "Narsingdi": [
        "Belabo",
        "Monohardi",
        "Narsingdi Sadar",
        "Palash",
        "Raipura",
        "Shibpur",
    ],

    "Rajbari": [
        "Baliakandi",
        "Goalanda",
        "Kalukhali",
        "Pangsha",
        "Rajbari Sadar",
    ],

    "Shariatpur": [
        "Bhedarganj",
        "Damudya",
        "Gosairhat",
        "Naria",
        "Shariatpur Sadar",
        "Zajira",
    ],

    "Tangail": [
        "Basail",
        "Bhuapur",
        "Delduar",
        "Dhanbari",
        "Ghatail",
        "Gopalpur",
        "Kalihati",
        "Madhupur",
        "Mirzapur",
        "Nagarpur",
        "Sakhipur",
        "Tangail Sadar",
    ],


    # =====================================================
    # KHULNA DIVISION
    # =====================================================

    "Bagerhat": [
        "Bagerhat Sadar",
        "Chitalmari",
        "Fakirhat",
        "Kachua",
        "Mollahat",
        "Mongla",
        "Morrelganj",
        "Rampal",
        "Sarankhola",
    ],

    "Chuadanga": [
        "Alamdanga",
        "Chuadanga Sadar",
        "Damurhuda",
        "Jibannagar",
    ],

    "Jashore": [
        "Abhaynagar",
        "Bagherpara",
        "Chaugachha",
        "Jhikargachha",
        "Keshabpur",
        "Jashore Sadar",
        "Manirampur",
        "Sharsha",
    ],

    "Jhenaidah": [
        "Harinakunda",
        "Jhenaidah Sadar",
        "Kaliganj",
        "Kotchandpur",
        "Maheshpur",
        "Shailkupa",
    ],

    "Khulna": [
        "Batiaghata",
        "Dacope",
        "Dighalia",
        "Dumuria",
        "Koyra",
        "Paikgachha",
        "Phultala",
        "Rupsa",
        "Terokhada",
    ],

    "Kushtia": [
        "Bheramara",
        "Daulatpur",
        "Khoksa",
        "Kumarkhali",
        "Kushtia Sadar",
        "Mirpur",
    ],

    "Magura": [
        "Magura Sadar",
        "Mohammadpur",
        "Shalikha",
        "Sreepur",
    ],

    "Meherpur": [
        "Gangni",
        "Mujibnagar",
        "Meherpur Sadar",
    ],

    "Narail": [
        "Kalia",
        "Lohagara",
        "Narail Sadar",
    ],

    "Satkhira": [
        "Assasuni",
        "Debhata",
        "Kalaroa",
        "Kaliganj",
        "Satkhira Sadar",
        "Shyamnagar",
        "Tala",
    ],


    # =====================================================
    # BARISHAL DIVISION
    # =====================================================

    "Barguna": [
        "Amtali",
        "Bamna",
        "Barguna Sadar",
        "Betagi",
        "Patharghata",
        "Taltali",
    ],

    "Barishal": [
        "Agailjhara",
        "Babuganj",
        "Bakerganj",
        "Banaripara",
        "Gaurnadi",
        "Hizla",
        "Barishal Sadar",
        "Mehendiganj",
        "Muladi",
        "Wazirpur",
    ],

    "Bhola": [
        "Bhola Sadar",
        "Borhanuddin",
        "Daulatkhan",
        "Lalmohan",
        "Manpura",
        "Tazumuddin",
        "Char Fasson",
    ],

    "Jhalokati": [
        "Jhalokati Sadar",
        "Nalchity",
        "Kathalia",
        "Rajapur",
    ],

    "Patuakhali": [
        "Bauphal",
        "Dashmina",
        "Dumki",
        "Kalapara",
        "Mirzaganj",
        "Patuakhali Sadar",
        "Rangabali",
        "Galachipa",
    ],

    "Pirojpur": [
        "Bhandaria",
        "Kawkhali",
        "Mathbaria",
        "Nazirpur",
        "Pirojpur Sadar",
        "Nesarabad",
        "Zianagar",
    ],


    # =====================================================
    # CHATTOGRAM DIVISION
    # =====================================================

    "Bandarban": [
        "Alikadam",
        "Bandarban Sadar",
        "Lama",
        "Naikhongchhari",
        "Rowangchhari",
        "Ruma",
        "Thanchi",
    ],

    "Brahmanbaria": [
        "Akhaura",
        "Bancharampur",
        "Bijoynagar",
        "Brahmanbaria Sadar",
        "Ashuganj",
        "Kasba",
        "Nabinagar",
        "Nasirnagar",
        "Sarail",
    ],

    "Chandpur": [
        "Chandpur Sadar",
        "Faridganj",
        "Haimchar",
        "Hajiganj",
        "Kachua",
        "Matlab Dakshin",
        "Matlab Uttar",
        "Shahrasti",
    ],

    "Chattogram": [
        "Anwara",
        "Banshkhali",
        "Boalkhali",
        "Chandanaish",
        "Fatikchhari",
        "Hathazari",
        "Lohagara",
        "Mirsharai",
        "Patiya",
        "Rangunia",
        "Raozan",
        "Sandwip",
        "Satkania",
        "Sitakunda",
        "Karnaphuli",
    ],

    "Cumilla": [
        "Barura",
        "Brahmanpara",
        "Burichang",
        "Chandina",
        "Chauddagram",
        "Cumilla Sadar Dakshin",
        "Cumilla Adarsha Sadar",
        "Daudkandi",
        "Debidwar",
        "Homna",
        "Laksam",
        "Monoharganj",
        "Meghna",
        "Muradnagar",
        "Nangalkot",
        "Titas",
        "Lalmai",
    ],

    "Cox's Bazar": [
        "Chakaria",
        "Cox's Bazar Sadar",
        "Eidgaon",
        "Kutubdia",
        "Maheshkhali",
        "Pekua",
        "Ramu",
        "Teknaf",
        "Ukhia",
        "Matamuhuri",
    ],

    "Feni": [
        "Chhagalnaiya",
        "Daganbhuiyan",
        "Feni Sadar",
        "Fulgazi",
        "Parshuram",
        "Sonagazi",
    ],

    "Khagrachhari": [
        "Dighinala",
        "Manikchhari",
        "Khagrachhari Sadar",
        "Lakshmichhari",
        "Mahalchhari",
        "Matiranga",
        "Panchhari",
        "Ramgarh",
        "Guimara",
    ],

    "Lakshmipur": [
        "Kamalnagar",
        "Lakshmipur Sadar",
        "Raipur",
        "Ramganj",
        "Ramgati",
        "Chandraganj",
    ],

    "Noakhali": [
        "Begumganj",
        "Chatkhil",
        "Companiganj",
        "Hatiya",
        "Senbagh",
        "Sonaimuri",
        "Subarnachar",
        "Noakhali Sadar",
        "Kabirhat",
    ],

    "Rangamati": [
        "Baghaichhari",
        "Barkal",
        "Kawkhali",
        "Kaptai",
        "Juraichhari",
        "Langadu",
        "Naniarchar",
        "Rangamati Sadar",
        "Rajasthali",
        "Belaichhari",
    ],


    # =====================================================
    # RAJSHAHI DIVISION
    # =====================================================

    "Bogra": [
        "Adamdighi",
        "Bogra Sadar",
        "Dhunat",
        "Dhupchanchia",
        "Gabtali",
        "Kahaloo",
        "Nandigram",
        "Sariakandi",
        "Shajahanpur",
        "Sherpur",
        "Shibganj",
        "Sonatala",
        "Mokamtala",
    ],

    "Joypurhat": [
        "Akkelpur",
        "Joypurhat Sadar",
        "Kalai",
        "Panchbibi",
        "Khetlal",
    ],

    "Naogaon": [
        "Atrai",
        "Dhamoirhat",
        "Manda",
        "Mahadebpur",
        "Naogaon Sadar",
        "Niamatpur",
        "Patnitala",
        "Raninagar",
        "Sapahar",
        "Badalgachhi",
        "Porsha",
    ],

    "Natore": [
        "Bagatipara",
        "Baraigram",
        "Gurudaspur",
        "Lalpur",
        "Natore Sadar",
        "Singra",
        "Naldanga",
    ],

    "Chapainawabganj": [
        "Bholahat",
        "Gomastapur",
        "Nachole",
        "Chapainawabganj Sadar",
        "Shibganj",
    ],

    "Pabna": [
        "Atgharia",
        "Bera",
        "Bhangura",
        "Chatmohar",
        "Faridpur",
        "Ishwardi",
        "Pabna Sadar",
        "Santhia",
        "Sujanagar",
    ],

    "Rajshahi": [
        "Bagha",
        "Bagmara",
        "Charghat",
        "Durgapur",
        "Godagari",
        "Mohanpur",
        "Paba",
        "Puthia",
        "Tanore",
    ],

    "Sirajganj": [
        "Belkuchi",
        "Chauhali",
        "Kamarkhanda",
        "Kazipur",
        "Raiganj",
        "Shahjadpur",
        "Sirajganj Sadar",
        "Tarash",
        "Ullapara",
    ],


    # =====================================================
    # SYLHET DIVISION
    # =====================================================

    "Habiganj": [
        "Ajmiriganj",
        "Bahubal",
        "Baniachong",
        "Chunarughat",
        "Habiganj Sadar",
        "Lakhai",
        "Madhabpur",
        "Nabiganj",
        "Shayestaganj",
    ],

    "Moulvibazar": [
        "Barlekha",
        "Juri",
        "Kamalganj",
        "Kulaura",
        "Moulvibazar Sadar",
        "Rajnagar",
        "Sreemangal",
    ],

    "Sunamganj": [
        "Bishwambharpur",
        "Chhatak",
        "Derai",
        "Dharampasha",
        "Dowarabazar",
        "Jagannathpur",
        "Jamalganj",
        "Shalla",
        "Sunamganj Sadar",
        "Tahirpur",
        "Shantiganj",
        "Madhyanagar",
    ],

    "Sylhet": [
        "Balaganj",
        "Beanibazar",
        "Bishwanath",
        "Companiganj",
        "Dakshin Surma",
        "Fenchuganj",
        "Golapganj",
        "Gowainghat",
        "Jaintiapur",
        "Kanaighat",
        "Sylhet Sadar",
        "Zakiganj",
        "Osmani Nagar",
    ],


    # =====================================================
    # RANGPUR DIVISION
    # =====================================================

    "Dinajpur": [
        "Birampur",
        "Birganj",
        "Biral",
        "Bochaganj",
        "Chirirbandar",
        "Fulbari",
        "Ghoraghat",
        "Hakimpur",
        "Kaharole",
        "Khansama",
        "Nawabganj",
        "Parbatipur",
        "Dinajpur Sadar",
    ],

    "Gaibandha": [
        "Fulchhari",
        "Gaibandha Sadar",
        "Gobindaganj",
        "Palashbari",
        "Sadullapur",
        "Saghata",
        "Sundarganj",
    ],

    "Kurigram": [
        "Bhurungamari",
        "Char Rajibpur",
        "Chilmari",
        "Phulbari",
        "Kurigram Sadar",
        "Nageshwari",
        "Rajarhat",
        "Raomari",
        "Ulipur",
    ],

    "Lalmonirhat": [
        "Aditmari",
        "Hatibandha",
        "Kaliganj",
        "Lalmonirhat Sadar",
        "Patgram",
    ],

    "Nilphamari": [
        "Domar",
        "Jaldhaka",
        "Kishoreganj",
        "Nilphamari Sadar",
        "Saidpur",
        "Dimla",
    ],

    "Panchagarh": [
        "Atwari",
        "Boda",
        "Debiganj",
        "Panchagarh Sadar",
        "Tetulia",
    ],

    "Rangpur": [
        "Badarganj",
        "Gangachara",
        "Kaunia",
        "Mithapukur",
        "Pirgachha",
        "Pirganj",
        "Rangpur Sadar",
        "Taraganj",
    ],

    "Thakurgaon": [
        "Baliadangi",
        "Haripur",
        "Pirganj",
        "Ranisankail",
        "Thakurgaon Sadar",
        "Bhullee",
        "Ruhia",
    ],


    # =====================================================
    # MYMENSINGH DIVISION
    # =====================================================

    "Jamalpur": [
        "Baksiganj",
        "Dewanganj",
        "Islampur",
        "Jamalpur Sadar",
        "Madarganj",
        "Melandaha",
        "Sarishabari",
    ],

    "Mymensingh": [
        "Bhaluka",
        "Dhobaura",
        "Fulbaria",
        "Gaffargaon",
        "Gauripur",
        "Haluaghat",
        "Ishwarganj",
        "Mymensingh Sadar",
        "Muktagachha",
        "Nandail",
        "Phulpur",
        "Tarakanda",
        "Trishal",
    ],

    "Netrokona": [
        "Atpara",
        "Barhatta",
        "Durgapur",
        "Khaliajuri",
        "Kalmakanda",
        "Kendua",
        "Madan",
        "Mohanganj",
        "Netrokona Sadar",
        "Purbadhala",
    ],

    "Sherpur": [
        "Jhenaigati",
        "Nakla",
        "Nalitabari",
        "Sherpur Sadar",
        "Sreebardi",
    ],


    # =====================================================
    # DHAKA CITY DELIVERY AREAS
    # =====================================================
    #
    # These are added on top of the official Dhaka district
    # upazilas because NAFI is an e-commerce business.
    #
    # This makes Dhaka checkout much more practical.
    #

}


# =========================================================
# DHAKA CITY DETAILED DELIVERY AREAS
# =========================================================

DHAKA_CITY_AREAS = [

    # -------------------------
    # Central / Old Dhaka
    # -------------------------
    "Kotwali",
    "Sutrapur",
    "Wari",
    "Gandaria",
    "Bangshal",
    "Lalbagh",
    "Chawkbazar",
    "Islampur",
    "Nazira Bazar",
    "Sadarghat",
    "Patuatuli",
    "Bakshibazar",

    # -------------------------
    # Dhanmondi / Mohammadpur
    # -------------------------
    "Dhanmondi",
    "Kalabagan",
    "Green Road",
    "Panthapath",
    "New Market",
    "Nilkhet",
    "Lalmatia",
    "Mohammadpur",
    "Adabor",
    "Shyamoli",
    "Asad Gate",
    "Kallyanpur",

    # -------------------------
    # Mirpur
    # -------------------------
    "Mirpur 1",
    "Mirpur 2",
    "Mirpur 6",
    "Mirpur 10",
    "Mirpur 11",
    "Mirpur 12",
    "Mirpur 13",
    "Mirpur 14",
    "Pallabi",
    "Kazipara",
    "Shewrapara",
    "Tolarbag",
    "Rupnagar",
    "Monipur",
    "Darus Salam",

    # -------------------------
    # Uttara
    # -------------------------
    "Uttara",
    "Uttara Sector 1",
    "Uttara Sector 3",
    "Uttara Sector 4",
    "Uttara Sector 5",
    "Uttara Sector 6",
    "Uttara Sector 7",
    "Uttara Sector 9",
    "Uttara Sector 10",
    "Uttara Sector 11",
    "Uttara Sector 12",
    "Uttara Sector 13",
    "Uttara Sector 14",
    "Airport",
    "Dakshinkhan",
    "Uttarkhan",

    # -------------------------
    # Gulshan / Banani
    # -------------------------
    "Gulshan",
    "Gulshan 1",
    "Gulshan 2",
    "Banani",
    "Banani DOHS",
    "Mohakhali",
    "Mohakhali DOHS",
    "Niketan",
    "Baridhara",
    "Baridhara DOHS",
    "Bashundhara",
    "Bashundhara R/A",

    # -------------------------
    # Badda / Rampura
    # -------------------------
    "Badda",
    "Middle Badda",
    "Merul Badda",
    "Uttar Badda",
    "Aftabnagar",
    "Rampura",
    "South Banasree",
    "Banasree",
    "Mouchak",
    "Malibagh",

    # -------------------------
    # Khilgaon / Motijheel
    # -------------------------
    "Khilgaon",
    "Taltola",
    "Basabo",
    "Mugda",
    "Manda",
    "Shahjahanpur",
    "Motijheel",
    "Dilkusha",
    "Paltan",
    "Kakrail",
    "Fakirapool",

    # -------------------------
    # Tejgaon / Farmgate
    # -------------------------
    "Tejgaon",
    "Tejgaon Industrial Area",
    "Farmgate",
    "Karwan Bazar",
    "Mohakhali",

    # -------------------------
    # Cantonment
    # -------------------------
    "Dhaka Cantonment",
    "Cantonment",
    "DOHS Mirpur",
    "DOHS Mohakhali",
    "DOHS Baridhara",

    # -------------------------
    # Khilkhet / Nikunja
    # -------------------------
    "Khilkhet",
    "Nikunja 1",
    "Nikunja 2",
    "Kuril",
    "Joar Sahara",

    # -------------------------
    # Jatrabari / Demra
    # -------------------------
    "Jatrabari",
    "Dhania",
    "Shampur",
    "Postogola",
    "Jurain",
    "Demra",
    "Matuail",
    "Sarulia",

    # -------------------------
    # Savar / Ashulia
    # -------------------------
    "Savar",
    "Ashulia",
    "Dhamsona",
    "Baipail",
    "Nabinagar",
    "Hemayetpur",
    "Amin Bazar",

    # -------------------------
    # Keraniganj
    # -------------------------
    "Keraniganj",
    "Zinzira",
    "Hasnabad",
    "Kalatia",

    # -------------------------
    # Other important areas
    # -------------------------
    "Kawran Bazar",
    "Shahbagh",
    "Ramna",
    "Segunbagicha",
    "Eskaton",
    "Moghbazar",
    "Hatirjheel",
    "Shantinagar",
    "Siddheshwari",
]


# =========================================================
# FINAL DISTRICT → AREA DATA
# =========================================================
#
# For all districts:
#     Official Upazila list
#
# For Dhaka:
#     Official Upazila list
#     +
#     detailed Dhaka city delivery areas
#
# =========================================================

DISTRICT_AREAS = {
    district: list(areas)
    for district, areas in OFFICIAL_UPAZILAS.items()
}


# Add detailed Dhaka delivery areas
DISTRICT_AREAS["Dhaka"] = list(
    dict.fromkeys(
        OFFICIAL_UPAZILAS["Dhaka"]
        + DHAKA_CITY_AREAS
    )
)


# =========================================================
# DISTRICT LIST
# =========================================================
# =========================================================
# ALPHABETICAL SORTING
# =========================================================

# District names → A-Z
DISTRICTS = sorted(
    OFFICIAL_UPAZILAS.keys(),
    key=str.casefold
)


# All areas inside every district → A-Z
for district in DISTRICT_AREAS:
    DISTRICT_AREAS[district] = sorted(
        DISTRICT_AREAS[district],
        key=str.casefold
    )

# =========================================================
# SAFETY / DATA VALIDATION
# =========================================================
#
# These checks run when Django imports this file.
# If the official base dataset is accidentally broken,
# Django will immediately show an error instead of silently
# using incomplete location data.
#
# =========================================================

assert len(DISTRICTS) == 64, (
    f"Location data error: expected 64 districts, "
    f"found {len(DISTRICTS)}."
)


TOTAL_OFFICIAL_UPAZILAS = sum(
    len(areas)
    for areas in OFFICIAL_UPAZILAS.values()
)


assert TOTAL_OFFICIAL_UPAZILAS == 500, (
    f"Location data error: expected 500 official upazilas, "
    f"found {TOTAL_OFFICIAL_UPAZILAS}."
)


# Check duplicate district names
assert len(DISTRICTS) == len(set(DISTRICTS)), (
    "Location data error: duplicate district found."
)


# Check duplicate official areas inside each district
for district, areas in OFFICIAL_UPAZILAS.items():

    assert len(areas) == len(set(areas)), (
        f"Location data error: duplicate area found "
        f"in {district}."
    )
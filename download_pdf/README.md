# Download PDF section

This part is purposed to scrape all pdf links stored in each website, download these files, and store them into different folders. 
Part of the codes are referred to the heatmap_create section and slightly revised. 

Here are some noteworthy tips that users should consider while they are implementing the code:
1. Your static IP address might be forbidden if you download too many files in using this code. Thus, dynamic IP is more preferable and safe for long-term downloading.
2. ScienceDirect only provides subscription-based access to all pdfs. If the user does not have the membership, implementing this code would only download a small fraction of free files, which, in some ways, prove my codes are completely legal. Generally, most colleges have the subscriptions. 
3. Using python to access the file is apparently different from using browser. Thus, we need to prove our identity and show the granted membership by displaying cookies (session_id in line 75, main.py). This part is much simpler if the user could manually operate it. Sciencedirect would give the user an identity cookie after the user has successfully signed in. In Google Chrome, for instance, the user could get access to that locally stored data under chrome://settings/siteData?search=cookie -> sciencedirect.com -> sd_session_id -> content. The user may just copy the string under content section and paste on line 75, main.py. There is only 2-days duration for this cookie, so the information should be periodically updated for long-term downloading.
4. Generally, the downloading speed is average 1 second per file. 
5. All I/O are written in full paths. The user may keep in mind and revise them to relative paths in cases of needed. 
6. All codes should be stored in the same folder before implementing. 
7. While collecting all downloadable URLs, we could also collect all hidden information about the articles (embedded in the website) and save it in script_data-well-format.json for future reference. 

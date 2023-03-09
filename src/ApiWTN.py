import json
import os
import subprocess

from src import get_project_root

linux = False
proxy = ""


def get_bearer():
    token_potpot = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..IHA9r3jTh8hOMTjB.7pBbH-SXpFF4i6on0nJ1eipYS7ocus5ntEw-Tg7KXIbmGWlidlRuK6LRzUuvCFAo-SYztVyX3_aQXVNBzXkLoB0oAT1cnUTcn0NR-llqu-hjhOCqBMaKcr77DQ3H3K3thYP_5f5jCc54ohsTtZSo6P7dwhwwGPlw8hniuDpWIYbRyq7PsxPnwdV1xN5A3MSLBFZE7gJq0r3QQN9ENZ0P0VuBBSZFi4SaBKX_2K_xpffabtTHTx8zkZi9m8h1sQ1m1Avz2D0gHZS9CsEvlC0OOyVkUXpNHan9a7l7RuSZ60l8uO2msudPgzSGDGZb0pEJ5CdcFXhTc7mYuHV9p5wk7NjrtnOq6feeQbSTDW15b0kuABznlJ1dI-LaoNWNde6t6oZv5fqif84Jf0kwvt-WJYDxfHXCst2nqixhRll3WHDCqHmZ5mHSgqu_W4hj-m-hoLpuZ7IoSi6JwI4TLoGt2SuuCbrX2jVtO2jR04p3dVqsah0Lghgo244tMFn0rDtaS9gXU-BsZ0KmG3zLvWCFFTysOTEtd9xkxjM9WeZggBkdj3otJPLdrTPq7NDKKEPdiMU3vVE0YbDyxio0X3I5iRLVXHnC4RAtkxxbBwyJns097fGN8wvDuMIlmLwOK5M1fk0wnwXWLQ2eQ9AuA5Q_7wykp5HirKtUHYHD9Uq6M3V8w0zqo00R1aLLXS7-uio_i_BaGlCTHQShiN_EFldYjSANSIMXrUYeRgmNlhKh4HjN3sS5--42JuC9bVa7V-pEJ4n41jGnPLHl3DrYpyC2r43eAw.FkWhlSUmRyo2E6OPTR-GXg"
    token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..-9AVVMQ61qe7r2DL.cln-0OafNC9KhCwDFiwT_vDJUbW84LF4r6QpzWwRWrTS1aZZbLDK1sKRaXqhrxAGm5W4ChVQj-bu5erE4zhSeFhRM2nKYeY3lQ0Y5WttKWfFYMPBQ0KJB742RAcH36GvBHWwi8M3Q0I7zI-pFx8BogrbCfFosv4OQAI28hwFIg24-gkIRDhlgIcMpqZBvpnVG2ySMiGHpNCwPjyMB-wkRJsSmpyVjY3-q4V64og86kglEnBqrCUdxeiNxKAx_lVCDIABnAClMm3bxRuafKZf0UJjI0W-wQ3p7rqyJkWL6ZyAgeiF5hc35sHoC1gL8Dom2ad1O1a_GH2ENMpO1nG3WqhqKxwpePjCTfUX0-zSOJUEAhiV1CxTPadzk8bOH3QYhIp2dJaQNzOG1tSyLiV_ptlISy3y10AoOJ9-QfCkTSNjpHCeu_RQ9jJ8WFmE7AWHDWOJ5A8OzErqTV0FtMVXsPKTMLcHcMsSO6dx-KyEJ8ZibJOiDKu3tfbO3ee9xAhvmXFsZ1XWJyAEJ2AjXfHiThczQJtYDZse29JZ3zCqD6yB0ujN1Njs9iDrwCxGsrIfnhTf6tzKGHq85gTpvGxugsIOw7IrPdsc6CFKqX8Q4_tKWyFrrwC7YmhvpU5buyPW_7ccqQOvY-FTBwqO90EFhcXnt8CVfbemy308SmOLDhx2uxexJGNOy_indz5O69HE6tKPb0jIN5QqQ2CzqYb0yr2D_prS5SK6rBa8bYEU3_VjWtIxR3t468s7Vm61._2vZJ4HDvRLPbqygFIJzug"
    token = token_potpot
    if linux:
        file_path = os.path.join(get_project_root(), "curl/linux/curl_chrome110")
        cmd = file_path + f" 'https://sell.wethenew.com/api/auth/session' \
-H 'authority: sell.wethenew.com' \
-H 'accept: */*' \
-H 'cookie: __Secure-next-auth.session-token={token}' \
-H 'dnt: 1' \
-H 'referer: https://sell.wethenew.com/fr/offers'"
    else:
        file_path = os.path.join(get_project_root(), "curl/windows/curl_chrome110.bat")
        cmd = file_path + f" https://sell.wethenew.com/api/auth/session ^\
-H \"authority: sell.wethenew.com\" ^\
-H \"accept: */*\" ^\
-H \"cookie: __Secure-next-auth.session-token={token}\" ^\
-H \"dnt: 1\" ^\
-H \"referer: https://sell.wethenew.com/fr/offers\""
    print(cmd)
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = run.stdout
    try:
        output_json = json.loads(output)
    except json.decoder.JSONDecodeError as e:
        print("Erreur lors de la requête vers l'API :")
        print(e)
        print("Exécution du script :")
        print(run.stderr)
        print(run.stdout)
        return
    print(output_json)
    if "user" not in output_json.keys():
        print("Erreur mauvais token")
        return
    bearer = output_json["user"]["accessToken"]
    print(bearer)
    return get_offers(bearer)


def get_offers(bearer: str):
    if linux:
        file_path = os.path.join(get_project_root(), "curl/linux/curl_chrome110")
        cmd = file_path + f" 'https://api-sell.wethenew.com/offers?skip=0' \
-H 'authority: api-sell.wethenew.com' \
-H 'accept: application/json, text/plain, */*' \
-H 'authorization: Bearer {bearer}' \
-H 'cache-control: no-cache' \
-H 'dnt: 1' \
-H 'origin: https://sell.wethenew.com' \
-H 'pragma: no-cache' \
-H 'referer: https://sell.wethenew.com/' \
-H 'x-xss-protection: 1;mode=block'"
    else:
        file_path = os.path.join(get_project_root(), "curl/windows/curl_chrome110.bat")
        cmd = file_path + f" https://api-sell.wethenew.com/offers?skip=0 ^\
-H \"authority: api-sell.wethenew.com\" ^\
-H \"accept: application/json, text/plain, */*\" ^\
-H \"authorization: Bearer {bearer}\" ^\
-H \"cache-control: no-cache\" ^\
-H \"dnt: 1\" ^\
-H \"origin: https://sell.wethenew.com\" ^\
-H \"pragma: no-cache\" ^\
-H \"referer: https://sell.wethenew.com/\" ^\
-H \"x-xss-protection: 1;mode=block\""
    print(cmd)
    # output: {"pagination":{"totalPages":0,"page":1,"itemsPerPage":25,"totalItems":0},"results":[]}
    run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = run.stdout
    try:
        output_json = json.loads(output)
    except json.decoder.JSONDecodeError as e:
        print("Erreur lors de la requête vers l'API :")
        print(e)
        print("Exécution du script :")
        print(run.stderr)
        print(run.stdout)
        return
    print(output_json)
    if "pagination" not in output_json.keys():
        print("Error: " + output_json["message"])
        return
    offers = output_json["pagination"]["totalItems"]
    if offers == 0:
        print(f"No offer ({offers})")
        return
    result = output_json["results"]
    print(f"Offers ({offers})")
    print(result)


def main():
    get_bearer()
    # get_offers("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Imh1Z29zbmVha2Vyc29mZkBnbWFpbC5jb20iLCJmaXJzdG5hbWUiOiJIdWdvIiwibGFzdG5hbWUiOiJQb3RpZXIiLCJpYXQiOjE2NzgyOTY5MTYsImV4cCI6MTY4MzQ4MDkxNn0.vIafP0INCnC8IPdESkSXXpiO4ZbCY9H0md3i0QJWKq0")


if __name__ == "__main__":
    main()
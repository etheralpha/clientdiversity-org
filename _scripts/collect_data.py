import requests
import os
import math
import time
import json
import copy
import pprint
from datetime import datetime, timezone


current_time = round(time.time()) # seconds
override_before_epoch = current_time < 1708115400
date = datetime.now(timezone.utc).strftime('%Y-%m-%d') # yyyy-mm-dd
day = time.strftime('%A', time.localtime(current_time)) # Sunday
print(f"Epoch: {current_time}")
print(f"Date: {date}")
print(f"Day: {day}")

pp = pprint.PrettyPrinter(indent=4)
use_test_data = False
print_fetch_data = False
print_processed_data = True
pretty_print = True
exit_on_fetch_error = False
exit_on_save_error = True
exit_on_report_error = False

rated_token = os.environ.get("RATED_API_KEY")
migalabs_token = os.environ.get("MIGALABS_TOKEN")
google_form_error_report_url = os.environ.get("ERROR_REPORT_ENDPOINT")

# enter values for local testing
# rated_token = ""
# google_form_error_report_url = ""


def fetch(url, method="GET", payload={}, headers={}, retries=2, data_type="json"):
  print(f"Fetch: {url}")
  response = {"status": 0, "attempts": 0, "data": None}
  try: 
    while response["attempts"] <= retries and (response["status"] != 200 or response["data"] == None):
      rate_limited_domains = ["rated.network"]
      rate_limited = any(domain in url for domain in rate_limited_domains)
      if (rate_limited or response["attempts"] > 0):
        time.sleep(1.05)
      response["attempts"] = response["attempts"] + 1
      r = requests.request(method, url, headers=headers, data=payload)
      if data_type == "json":
        response = {"status": r.status_code, "attempts": response["attempts"], "data": r.json()}
      elif data_type == "text":
        response = {"status": r.status_code, "attempts": response["attempts"], "data": r.text}
      else:
        response = {"status": r.status_code, "attempts": response["attempts"], "data": r.content}
  except:
    error = f"Fetch failed: {url}"
    report_error(error)
    if exit_on_fetch_error:
      raise SystemExit(error)
    else:
      print(error)
  finally:
    print_data("fetch", response, label=None)
    return response

def save_to_file(rel_path, data):
  if not rel_path.startswith("/"):
    rel_path = "/" + rel_path
  abs_path = os.path.dirname(__file__) + rel_path
  # skip file save if using test data
  if use_test_data:
    return
  else:
    todays_data =  {
      "date":date,
      "timestamp":current_time,
      "data":data
    }
    # check if file exists yet
    if os.path.isfile(abs_path):
      try:
        with open(abs_path, 'r') as f:
          all_data = json.load(f)
          # check if there's already data for today
          if date != all_data[-1]['date'] and all_data[-1]['data'] != None:
            # append todays data to historical data and write to file
            all_data.append(todays_data)
            with open(abs_path, 'w') as f:
              json.dump(all_data, f, indent=None, separators=(',', ':'))
            f.close()
            print(f"{rel_path} data has been updated")
          # if the data was null or override set then overwrite last entry
          elif date == all_data[-1]['date'] and (all_data[-1]['data'] == None or override_before_epoch):
            del all_data[-1]
            # append todays data to historical data and write to file
            all_data.append(todays_data)
            with open(abs_path, 'w') as f:
              json.dump(all_data, f, indent=None, separators=(',', ':'))
            f.close()
            print(f"{rel_path} data has been updated")
          else:
            print(f"{rel_path} data for the current date was already recorded")
      except:
        # file is empty or malformed data
        error = f"ERROR: {rel_path} file read error"
        report_error(error)
        if exit_on_save_error:
          raise SystemExit(error)
        else:
          print(error)
    else:
      # create new file with today's data
      all_data = []
      all_data.append(todays_data)
      with open(abs_path, 'w') as f:
        json.dump(all_data, f, indent=None, separators=(',', ':'))
      f.close()
      print(f"{rel_path} data has been updated")

def report_error(error, context=""):
  if use_test_data:
    return
  else:
    data = {
      # "entry.2112281434": "name",    # text
      # "entry.1600556346": "option3", # dropdown
      # "entry.819260047": ["option2", "option3"], #checkbox multiple
      # "entry.1682233942": "option5"  # checkbox single
      "entry.76518486": error,
      "entry.943255668": context
    }
    try:
      requests.post(google_form_error_report_url, data)
      print("Error submitted")
    except:
      error = f"ERROR: {path} file read error"
      if exit_on_report_error:
        raise SystemExit(error)
      else:
        print(error)


def print_file(rel_path):
  # add leading / to relative path if not present
  if not rel_path.startswith("/"):
    rel_path = "/" + rel_path
  abs_path = os.path.dirname(__file__) + rel_path
  if os.path.isfile(abs_path):
    with open(abs_path, 'r') as f:
      contents = json.load(f)
      if pretty_print:
        pprint(contents)
      else:
        print(contents)
  else:
    print("not file")

def print_data(context, data, label=None):
  if context == "fetch" and print_fetch_data:
    if label:
      print(f"{label}:")
    if pretty_print:
      pp.pprint(data)
    else:
      print(data)
  if context == "processed" and print_processed_data:
    if label:
      print(f"{label}:")
    if pretty_print:
      pp.pprint(data)
    else:
      print(data)

def pprint(data):
  pp.pprint(data)


########################################
# RATED
########################################


def get_rated_marketshare_data():
  if use_test_data:
    # response split into multiple lines so it can be collapsed
    response = {
      'status': 200, 'attempts': 1, 'data': [
      {'timeWindow': 'all', 'validatorCount': 732484, 'validatorCountDiff': 0, 'medianValidatorAgeDays': 311, 'activeStake': 23439488000000000, 'activeStakeDiff': 0, 'avgValidatorBalance': 32139253647.151455, 'avgValidatorBalanceDiff': 0.0, 'consensusLayerRewardsPercentage': 70.89001418712094, 'priorityFeesPercentage': 22.444404751981917, 'baselineMevPercentage': 6.665581060897138, 'avgValidatorEffectiveness': 96.34926615541492, 'avgInclusionDelay': 1.02674142057442, 'avgUptime': 99.64490933047226, 'sumMissedSlots': 72749, 'missedSlotsPercentage': 1.022675595110489, 'avgConsensusAprPercentage': 3.5752906143040857, 'avgExecutionAprPercentage': 1.4681427314232345, 'medianConsensusAprPercentage': 3.466286508072917, 'medianExecutionAprPercentage': 0.4706290926215278, 'consensusRewardsRatio': 0.7089001418712094, 'executionRewardsRatio': 0.2910998581287906, 'avgNetworkAprPercentage': 5.04343334572732, 'medianNetworkAprPercentage': 3.936915600694445, 'avgConsensusAprGwei': 1144092997, 'avgExecutionAprGwei': 469805674, 'medianConsensusAprGwei': 1109211683, 'medianExecutionAprGwei': 150601310, 'avgNetworkAprGwei': 1613898671, 'medianNetworkAprGwei': 1259812992, 'giniCoefficient': 0.9593938319220118, 'clientPercentages': [{'client': 'Teku', 'percentage': 0.18995044012847778}, {'client': 'Lighthouse', 'percentage': 0.3653671935935509}, {'client': 'Nimbus', 'percentage': 0.03222118333276813}, {'client': 'Prysm', 'percentage': 0.401267821933271}, {'client': 'Lodestar', 'percentage': 0.011193361011932157}], 'clientValidatorEffectiveness': [{'client': 'Teku', 'avgValidatorEffectiveness': 97.38093}, {'client': 'Prysm', 'avgValidatorEffectiveness': 97.11941}, {'client': 'Nimbus', 'avgValidatorEffectiveness': 96.08916}, {'client': 'Lodestar', 'avgValidatorEffectiveness': 97.52908}, {'client': 'Lighthouse', 'avgValidatorEffectiveness': 97.25144}], 'latestEpoch': 222326, 'activationQueueMinutes': 37802.66667, 'activatingValidators': 63443, 'activatingStake': 2030176000000000, 'exitQueueMinutes': 32.0, 'withdrawalQueueMinutes': 1644.8, 'withdrawalProcessingQueueMinutes': 10400.825, 'fullyWithdrawingValidators': 585, 'partiallyWithdrawingValidators': 699897, 'totalWithdrawingValidators': 700482, 'fullyWithdrawingBalance': 24895807435429, 'partiallyWithdrawingBalance': 6499611370618, 'totalWithdrawingBalance': 31395418806047, 'exitingValidators': 2, 'exitingStake': 64000000000}, {'timeWindow': '7d', 'validatorCount': 732484, 'validatorCountDiff': 15285, 'medianValidatorAgeDays': 311, 'activeStake': 23439488000000000, 'activeStakeDiff': 489120000000000, 'avgValidatorBalance': 32139253647.151455, 'avgValidatorBalanceDiff': -1584026.892314911, 'consensusLayerRewardsPercentage': 74.17879638365959, 'priorityFeesPercentage': 18.16255691339244, 'baselineMevPercentage': 7.658646702947978, 'avgValidatorEffectiveness': 96.96456915550357, 'avgInclusionDelay': 1.0233240107783756, 'avgUptime': 99.5917567250837, 'sumMissedSlots': 356, 'missedSlotsPercentage': 0.7063492063492063, 'avgConsensusAprPercentage': 3.3712964163931844, 'avgExecutionAprPercentage': 1.1735284941601334, 'medianConsensusAprPercentage': 2.8652880479910716, 'medianExecutionAprPercentage': 0.0, 'consensusRewardsRatio': 0.7417879638365958, 'executionRewardsRatio': 0.25821203616340416, 'avgNetworkAprPercentage': 4.544824910553318, 'medianNetworkAprPercentage': 2.8652880479910716, 'avgConsensusAprGwei': 1078814853, 'avgExecutionAprGwei': 375529118, 'medianConsensusAprGwei': 916892175, 'medianExecutionAprGwei': 0, 'avgNetworkAprGwei': 1454343971, 'medianNetworkAprGwei': 916892175, 'giniCoefficient': 0.9593938319220118, 'clientPercentages': [{'client': 'Teku', 'percentage': 0.18995044012847778}, {'client': 'Lighthouse', 'percentage': 0.3653671935935509}, {'client': 'Nimbus', 'percentage': 0.03222118333276813}, {'client': 'Prysm', 'percentage': 0.401267821933271}, {'client': 'Lodestar', 'percentage': 0.011193361011932157}], 'clientValidatorEffectiveness': [{'client': 'Lighthouse', 'avgValidatorEffectiveness': 97.25144}, {'client': 'Lodestar', 'avgValidatorEffectiveness': 97.52908}, {'client': 'Nimbus', 'avgValidatorEffectiveness': 96.08916}, {'client': 'Prysm', 'avgValidatorEffectiveness': 97.11941}, {'client': 'Teku', 'avgValidatorEffectiveness': 97.38093}], 'latestEpoch': 222326, 'activationQueueMinutes': 37802.66667, 'activatingValidators': 63443, 'activatingStake': 2030176000000000, 'exitQueueMinutes': 32.0, 'withdrawalQueueMinutes': 1644.8, 'withdrawalProcessingQueueMinutes': 10400.825, 'fullyWithdrawingValidators': 585, 'partiallyWithdrawingValidators': 699897, 'totalWithdrawingValidators': 700482, 'fullyWithdrawingBalance': 24895807435429, 'partiallyWithdrawingBalance': 6499611370618, 'totalWithdrawingBalance': 31395418806047, 'exitingValidators': 2, 'exitingStake': 64000000000}, {'timeWindow': '30d', 'validatorCount': 732484, 'validatorCountDiff': 60820, 'medianValidatorAgeDays': 311, 'activeStake': 23439488000000000, 'activeStakeDiff': 1946240000000000, 'avgValidatorBalance': 32139253647.151455, 'avgValidatorBalanceDiff': -2782230.2838668823, 'consensusLayerRewardsPercentage': 70.19038984546984, 'priorityFeesPercentage': 20.892577953835676, 'baselineMevPercentage': 8.917032200694484, 'avgValidatorEffectiveness': 97.08324599003156, 'avgInclusionDelay': 1.0218653815464485, 'avgUptime': 99.60600150408419, 'sumMissedSlots': 1589, 'missedSlotsPercentage': 0.7356481481481482, 'avgConsensusAprPercentage': 3.4431767042864805, 'avgExecutionAprPercentage': 1.462304960464106, 'medianConsensusAprPercentage': 2.9132289458333336, 'medianExecutionAprPercentage': 0.0, 'consensusRewardsRatio': 0.7019038984546984, 'executionRewardsRatio': 0.29809610154530164, 'avgNetworkAprPercentage': 4.905481664750587, 'medianNetworkAprPercentage': 2.9132289458333336, 'avgConsensusAprGwei': 1101816545, 'avgExecutionAprGwei': 467937587, 'medianConsensusAprGwei': 932233263, 'medianExecutionAprGwei': 0, 'avgNetworkAprGwei': 1569754133, 'medianNetworkAprGwei': 932233263, 'giniCoefficient': 0.9593938319220118, 'clientPercentages': [{'client': 'Teku', 'percentage': 0.18995044012847778}, {'client': 'Lighthouse', 'percentage': 0.3653671935935509}, {'client': 'Nimbus', 'percentage': 0.03222118333276813}, {'client': 'Prysm', 'percentage': 0.401267821933271}, {'client': 'Lodestar', 'percentage': 0.011193361011932157}], 'clientValidatorEffectiveness': [{'client': 'Lighthouse', 'avgValidatorEffectiveness': 97.25144}, {'client': 'Teku', 'avgValidatorEffectiveness': 97.38093}, {'client': 'Prysm', 'avgValidatorEffectiveness': 97.11941}, {'client': 'Nimbus', 'avgValidatorEffectiveness': 96.08916}, {'client': 'Lodestar', 'avgValidatorEffectiveness': 97.52908}], 'latestEpoch': 222326, 'activationQueueMinutes': 37802.66667, 'activatingValidators': 63443, 'activatingStake': 2030176000000000, 'exitQueueMinutes': 32.0, 'withdrawalQueueMinutes': 1644.8, 'withdrawalProcessingQueueMinutes': 10400.825, 'fullyWithdrawingValidators': 585, 'partiallyWithdrawingValidators': 699897, 'totalWithdrawingValidators': 700482, 'fullyWithdrawingBalance': 24895807435429, 'partiallyWithdrawingBalance': 6499611370618, 'totalWithdrawingBalance': 31395418806047, 'exitingValidators': 2, 'exitingStake': 64000000000}, {'timeWindow': '1d', 'validatorCount': 732484, 'validatorCountDiff': 2183, 'medianValidatorAgeDays': 311, 'activeStake': 23439488000000000, 'activeStakeDiff': 69856000000000, 'avgValidatorBalance': 32139253647.151455, 'avgValidatorBalanceDiff': 220670.82093429565, 'consensusLayerRewardsPercentage': 68.76553541277683, 'priorityFeesPercentage': 22.120531489097694, 'baselineMevPercentage': 9.113933098125479, 'avgValidatorEffectiveness': 97.30381474144272, 'avgInclusionDelay': 1.0206948586335172, 'avgUptime': 99.64239298136275, 'sumMissedSlots': 51, 'missedSlotsPercentage': 0.7083333333333333, 'avgConsensusAprPercentage': 3.3542611110708775, 'avgExecutionAprPercentage': 1.5235619014838189, 'medianConsensusAprPercentage': 2.8587050937500003, 'medianExecutionAprPercentage': 0.0, 'consensusRewardsRatio': 0.6876553541277683, 'executionRewardsRatio': 0.3123446458722317, 'avgNetworkAprPercentage': 4.877823012554696, 'medianNetworkAprPercentage': 2.8587050937500003, 'avgConsensusAprGwei': 1073363556, 'avgExecutionAprGwei': 487539808, 'medianConsensusAprGwei': 914785630, 'medianExecutionAprGwei': 0, 'avgNetworkAprGwei': 1560903364, 'medianNetworkAprGwei': 914785630, 'giniCoefficient': 0.9593938319220118, 'clientPercentages': [{'client': 'Teku', 'percentage': 0.18995044012847778}, {'client': 'Lighthouse', 'percentage': 0.3653671935935509}, {'client': 'Nimbus', 'percentage': 0.03222118333276813}, {'client': 'Prysm', 'percentage': 0.401267821933271}, {'client': 'Lodestar', 'percentage': 0.011193361011932157}], 'clientValidatorEffectiveness': [{'client': 'Lighthouse', 'avgValidatorEffectiveness': 97.25144}, {'client': 'Lodestar', 'avgValidatorEffectiveness': 97.52908}, {'client': 'Nimbus', 'avgValidatorEffectiveness': 96.08916}, {'client': 'Prysm', 'avgValidatorEffectiveness': 97.11941}, {'client': 'Teku', 'avgValidatorEffectiveness': 97.38093}], 'latestEpoch': 222326, 'activationQueueMinutes': 37802.66667, 'activatingValidators': 63443, 'activatingStake': 2030176000000000, 'exitQueueMinutes': 32.0, 'withdrawalQueueMinutes': 1644.8, 'withdrawalProcessingQueueMinutes': 10400.825, 'fullyWithdrawingValidators': 585, 'partiallyWithdrawingValidators': 699897, 'totalWithdrawingValidators': 700482, 'fullyWithdrawingBalance': 24895807435429, 'partiallyWithdrawingBalance': 6499611370618, 'totalWithdrawingBalance': 31395418806047, 'exitingValidators': 2, 'exitingStake': 64000000000}]}
    print_data("fetch", response)
    return response
  else:
    url = "https://api.rated.network/v0/eth/network/overview"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': rated_token
    }
    response = fetch(url, "GET", payload, headers)
    return response

def process_rated_marketshare_data(raw_data):
  # example rated raw data:
  # raw_data = {'attempts': 1,'data': [
    # {'clientPercentages': [                   
    #   {'client': 'Teku',
    #   'percentage': 0.18995044012847778},
    #   {'client': 'Lighthouse',
    #   'percentage': 0.3653671935935509},
    #   {'client': 'Nimbus',
    #   'percentage': 0.03222118333276813},
    #   {'client': 'Prysm',
    #   'percentage': 0.401267821933271},
    #   {'client': 'Lodestar',
    #   'percentage': 0.011193361011932157}],

  main_clients = ["geth", "erigon", "nethermind", "besu", "reth"]
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  sample_size = 0
  reformatted_data = []
  filtered_data = [{"name": "other", "value": 0}]
  marketshare_data = []
  extra_data = {}
  final_data = {}

  # reformat data into a list of dicts
  for item in raw_data["data"][0]["clientPercentages"]:
    reformatted_data.append({"name": item["client"].lower(), "value": item["percentage"]})
  # pprint(["reformatted_data", reformatted_data])

  # filter out items either under the threshold and not in the main_clients list
  for item in reformatted_data:
    if item["name"] in main_clients:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    elif (item["value"] * 100) >= threshold_percentage:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    else:
      filtered_data[0]["value"] += item["value"]
  # pprint(["filtered_data", filtered_data])

  # calculate the marketshare for each client
  for item in filtered_data:
    marketshare = item["value"]
    marketshare_data.append({"name": item["name"], "value": marketshare, "accuracy": "no data"})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "rated"
  extra_data["has_majority"] = False
  extra_data["has_supermajority"] = False
  extra_data["danger_client"] = ""
  if sorted_data[0]["value"] >= .50:
    extra_data["has_majority"] = True
    extra_data["danger_client"] = sorted_data[0]["name"]
  if sorted_data[0]["value"] >= .66:
    extra_data["has_supermajority"] = True
  extra_data["top_client"] = sorted_data[0]["name"]
  # pprint(["extra_data", extra_data])

  # create final data dict
  final_data["distribution"] = sorted_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_rated")

  return final_data

def rated_marketshare():
  raw_data = get_rated_marketshare_data()
  save_to_file("../_data/raw/rated_raw.json", raw_data)
  processed_data = process_rated_marketshare_data(raw_data)
  save_to_file("../_data/rated.json", processed_data)


########################################
# SUPERMAJORITY
########################################


def get_supermajority_marketshare_data():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': [
      {"name":"Allnodes","website":"https://allnodes.com/eth2/staking","source":"https://twitter.com/Allnodes/status/1750519886286295117","twitter":"https://twitter.com/Allnodes","allocation":[{"name":"Besu","count":23895}]},{"name":"Blockdaemon","website":"https://blockdaemon.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/BlockdaemonHQ","allocation":[{"name":"Geth","count":9807}]},{"name":"Attestant","website":"https://www.attestant.io","source":"https://www.attestant.io/posts/helping-client-diversity","twitter":"https://twitter.com/attestantio","allocation":[{"name":"Nethermind","count":5000},{"name":"Besu","count":5001}]},{"name":"Blockscape","website":"https://blockscape.network","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/BlockscapeLab","allocation":[{"name":"Geth","count":8548},{"name":"Nethermind","count":1210}]},{"name":"BridgeTower","website":"https://bridgetowercapital.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/BridgeTowerCap","allocation":[{"name":"Geth","count":9600}]},{"name":"ChainLayer","website":"https://chainlayer.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/chainlayerio","allocation":[{"name":"Geth","count":8107},{"name":"Nethermind","count":1700}]},{"name":"ChainSafe","website":"https://chainsafe.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/ChainSafeth","allocation":[{"name":"Geth","count":6865},{"name":"Nethermind","count":2942}]},{"name":"Chorus One","website":"https://chorus.one","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/chorusone","allocation":[{"name":"Geth","count":9807}]},{"name":"Consensys","website":"https://consensys.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/consensys","allocation":[{"name":"Geth","count":8875}]},{"name":"CryptoManufaktur","website":"https://cryptomanufaktur.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/cryptomanuf","allocation":[{"name":"Nethermind","count":6538},{"name":"Besu","count":3269}]},{"name":"DSRV","website":"https://dsrvlabs.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/dsrvlabs","allocation":[{"name":"Geth","count":8024},{"name":"Nethermind","count":1783}]},{"name":"Everstake","website":"https://everstake.one","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/everstake_pool","allocation":[{"name":"Geth","count":9307},{"name":"Nethermind","count":500}]},{"name":"Figment","website":"https://figment.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/Figment_io","allocation":[{"name":"Geth","count":4904},{"name":"Erigon","count":4903}]},{"name":"HashKey Cloud","website":"https://hashkey.cloud/","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/HashKeyCloud","allocation":[{"name":"Geth","count":9807}]},{"name":"InfStones","website":"https://infstones.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/infstones","allocation":[{"name":"Geth","count":9807}]},{"name":"Jump Crypto","website":"https://jumpcrypto.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/jump_","allocation":[{"name":"Geth","count":1000}]},{"name":"Kiln","website":"https://kiln.fi","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/Kiln_finance","allocation":[{"name":"Geth","count":36754}]},{"name":"Kukis Global","website":"https://kukis-global.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/KukisGlobal","allocation":[{"name":"Geth","count":9807}]},{"name":"Launchnodes","website":"https://launchnodes.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/launchnodes","allocation":[{"name":"Besu","count":2562}]},{"name":"Nethermind","website":"https://nethermind.io","source":"https://twitter.com/tkstanczak/status/1750026116470030360","twitter":"https://twitter.com/NethermindEth","allocation":[{"name":"Nethermind","count":10001}]},{"name":"P2P.org","website":"https://p2p.org/networks/ethereum","source":"https://twitter.com/P2Pvalidator/status/1750550082934472885","twitter":"https://twitter.com/p2pvalidator","allocation":[{"name":"Besu","count":17927}]},{"name":"Prysmatic Labs","website":"https://prysmaticlabs.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/prylabs","allocation":[{"name":"Geth","count":9807}]},{"name":"RockLogic","website":"https://rocklogic.at","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/rocklogicgmbh","allocation":[{"name":"Geth","count":800},{"name":"Nethermind","count":2000},{"name":"Besu","count":1500},{"name":"Besu","count":1489}]},{"name":"RockX","website":"https://rockx.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/rockx_official","allocation":[{"name":"Geth","count":9107},{"name":"Nethermind","count":701}]},{"name":"SenseiNode","website":"https://senseinode.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/senseinode","allocation":[{"name":"Nethermind","count":100}]},{"name":"Sigma Prime","website":"https://sigmaprime.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/sigp_io","allocation":[{"name":"Geth","count":7043},{"name":"Nethermind","count":2764}]},{"name":"Simply Staking","website":"https://simplystaking.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/SimplyStaking","allocation":[{"name":"Geth","count":6465},{"name":"Nethermind","count":3036}]},{"name":"Stakefish","website":"https://stake.fish","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/stakefish","allocation":[{"name":"Geth","count":5878},{"name":"Nethermind","count":2938}]},{"name":"Stakely","website":"https://stakely.io","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/Stakely_io","allocation":[{"name":"Geth","count":3000},{"name":"Nethermind","count":4807},{"name":"Erigon","count":2000}]},{"name":"Stakin","website":"https://stakin.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/StakinOfficial","allocation":[{"name":"Besu","count":9807}]},{"name":"Staking Facilities","website":"https://stakingfacilities.com","source":"https://app.hex.tech/8dedcd99-17f4-49d8-944e-4857a355b90a/app/3f7d6967-3ef6-4e69-8f7b-d02d903f045b/latest","twitter":"https://twitter.com/stakingfac","allocation":[{"name":"Geth","count":8400}]},{"name":"Ethpool","website":"https://ethpool.org","source":"https://ethpool.org/faq","twitter":"https://twitter.com/ethpool_staking","allocation":[{"name":"Nethermind","count":3314}]},{"name":"Rocket Pool","website":"https://rocketpool.net","source":"https://discord.gg/BH2neAuw","twitter":"https://twitter.com/Rocket_Pool","allocation":[{"name":"Geth","count":7995},{"name":"Nethermind","count":6394},{"name":"Besu","count":2859},{"name":"Unknown","count":6405}]},{"name":"Coinbase","website":"https://www.coinbase.com/earn/staking/ethereum","source":"https://www.coinbase.com/de/cloud/discover/customer-stories/cb-wallet","twitter":"https://twitter.com/coinbase","allocation":[{"name":"Geth","count":135902}]},{"name":"Bitcoin Suisse","website":"https://bitcoinsuisse.com","twitter":"https://twitter.com/bitcoinsuisseag","allocation":[{"name":"Unknown","count":14602}]},{"name":"Kraken","website":"https://kraken.com","twitter":"https://twitter.com/krakenfx","allocation":[{"name":"Unknown","count":25968}]},{"name":"Binance","website":"https://binance.com","twitter":"https://twitter.com/binance","allocation":[{"name":"Unknown","count":34945}]},{"name":"OKX","website":"https://okx.com","twitter":"https://twitter.com/okx","allocation":[{"name":"Unknown","count":16141}]},{"name":"Blox Staking","website":"https://bloxstaking.com","source":"https://discord.com/channels/973544250828546069/1146751094433787964/1199615241949036604","allocation":[{"name":"Geth","count":4801}]}
    ]}
    print_data("fetch", response)
    return response
  else:
    url = "https://raw.githubusercontent.com/one-three-three-seven/Supermajority/main/public/services.json"
    response = fetch(url)
    return response

def get_supermajority_total_validators():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': "import { numberToPercent, type Distribution, type Service } from '@/lib'\nimport { ref, computed, type Ref } from 'vue'\nimport { defineStore } from 'pinia'\n\nconst totalValidators = 914433\n\nexport const useDistributionStore = defineStore('distribution', () => {\n    const services: Ref<Service[]> = ref([])\n\n    const allocation = computed(() => {\n        const map = new Map<string, number>().set('Unknown', 0).set('Geth', 0).set('Nethermind', 0).set('Besu', 0).set('Erigon', 0).set('Reth', 0)\n\n        services.value.forEach(service => {\n            service.allocation.forEach(client => {\n                map.set(client.name, (map.get(client.name) || 0) + client.count);\n            })\n        })\n\n        return map\n    })\n\n    const knwonDistribution = computed(() => distribution(true))\n    const completeDistribution = computed(() => distribution(false))\n\n    const distribution = (knownOnly = false) => {\n        const list: Distribution[] = []\n\n        allocation.value.forEach((count, name) => {\n            if (count && !(knownOnly && name === 'Unknown')) {\n                const share = count / ((knownOnly) ? knownValidators.value : totalValidators)\n\n                list.push({\n                    name,\n                    count,\n                    share: share * 100,\n                    shareFormatted: numberToPercent.format(share)\n                })\n            }\n        })\n\n        return list\n    }\n\n    const knownValidators = computed(() => {\n        let known = 0;\n\n        allocation.value.forEach((count, name) => {\n            if (name !== 'Unknown') {\n                known += count;\n            }\n        })\n\n        return known\n    })\n\n    const knownDistributionShareFormatted = computed(() => {\n        return numberToPercent.format(knownValidators.value / totalValidators)\n    })\n\n    const sortedServices = computed(() => {\n        const copy = [...services.value]\n\n        // Calculate total number of validators and the market share\n        const count = (service: Service) => service.allocation.reduce((total, client) => total + client.count, 0)\n        copy.forEach(service => {\n            const validators = count(service)\n            service.validators = validators\n            service.marketShareFormatted = numberToPercent.format(validators / totalValidators)\n        })\n\n        copy.sort((a, b) => {\n            if (a.validators === b.validators)"}
    print_data("fetch", response)
    return response
  else:
    url = "https://raw.githubusercontent.com/one-three-three-seven/Supermajority/47cfc175d15764b3dca30cf1e0a24c7abc2379ab/src/stores/distribution.ts"
    response = fetch(url, data_type="text")
    return response

def process_supermajority_total_validators(raw_data):
  before = "const totalValidators = "
  after = "\n"
  total_validators = raw_data["data"].split(before)[1].split(after)[0]
  # pprint(["total_validators", total_validators])
  return int(total_validators)

def process_supermajority_marketshare_data(raw_data, total_validators):
  # example supermajority raw data:
    # raw_data = {'status': 200, 'attempts': 1, 'data': [
    #   {
    #     "name":"Allnodes",
    #     "website":"https://allnodes.com/eth2/staking",
    #     "source":"https://twitter.com/Allnodes/status/1750519886286295117",
    #     "twitter":"https://twitter.com/Allnodes",
    #     "allocation":[
    #       {"name":"Besu","count":23895}
    #     ]
    #   }
    #   ...
    #   ]}

  main_clients = ["geth", "erigon", "nethermind", "besu", "reth"]
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  cleaned_data = {}
  sample_size = 0
  sample_size_all = 0
  reformatted_data = []
  filtered_data = [{"name": "other", "value": 0}]
  adjusted_data = []
  marketshare_data = []
  extra_data = {}
  final_data = {}
  # pprint(["total_validators", total_validators])

  # clean data
  for item in raw_data["data"]:
    for client in item["allocation"]:
      client_name = client["name"].lower()
      if client_name in cleaned_data:
        cleaned_data[client_name] += client["count"]
      else:
        cleaned_data[client_name] = client["count"]
      sample_size_all += client["count"]
      if client["name"].lower() != "unknown":
        sample_size += client["count"]
  # pprint(["cleaned_data", cleaned_data])
  # pprint(["sample_size", sample_size])
  # pprint(["sample_size_all", sample_size_all])

  # reformat data into a list of dicts
  for key, value in cleaned_data.items():
    reformatted_data.append({"name": key, "value": value})
  # pprint(["reformatted_data", reformatted_data])

  # filter out items either under the threshold and not in the main_clients list
  for item in reformatted_data:
    if item["name"] in main_clients or item["name"] == "unknown":
      filtered_data.append({"name": item["name"], "value": item["value"]})
    elif (item["value"] / sample_size * 100) >= threshold_percentage and item["name"] != "unknown":
      filtered_data.append({"name": item["name"], "value": item["value"]})
    elif item["name"] != "unknown":
      filtered_data[0]["value"] += item["value"]
  # pprint(["filtered_data", filtered_data])

  # adjust data where unaccounted validators are assumed 40% geth, 40% nethermind, and the rest is split
  remaining_validators = total_validators - sample_size_all
  remaining_geth_validators = round(remaining_validators * 0.4)
  remaining_nethermind_validators = round(remaining_validators * 0.4)
  unknown_validators = next((item for item in filtered_data if item['name'] == "unknown"), None)["value"]
  geth_adjusted = remaining_geth_validators + unknown_validators
  nethermind_adjusted = remaining_nethermind_validators

  split_size = 0
  for item in filtered_data:
    if item["name"] != "geth" and item["name"] != "nethermind" and item["name"] != "unknown" and item["name"] != "other":
      split_size += 1
  for item in filtered_data:
    if item["name"] == "geth":
      geth_adjusted += item["value"]
      adjusted_data.append({"name": item["name"], "value": geth_adjusted})
    elif item["name"] == "nethermind":
      nethermind_adjusted += item["value"]
      adjusted_data.append({"name": item["name"], "value": nethermind_adjusted})
    elif item["name"] == "other":
      adjusted_data.append({"name": item["name"], "value": item["value"]})
    elif item["name"] != "unknown":
      adjusted_value = round(remaining_validators * 0.2 / split_size) + item["value"]
      adjusted_data.append({"name": item["name"], "value": adjusted_value})
  # pprint(["remaining_validators", remaining_validators])
  # pprint(["remaining_geth_validators", remaining_geth_validators])
  # pprint(["unknown_validators", unknown_validators])
  # pprint(["geth_adjusted", geth_adjusted])
  # pprint(["nethermind_adjusted", nethermind_adjusted])
  # pprint(["split_size", split_size])
  # pprint(["adjusted_data", adjusted_data])


  # calculate the marketshare for each client
  for item in adjusted_data:
    marketshare = item["value"] / total_validators
    marketshare_data.append({"name": item["name"], "value": marketshare, "accuracy": "no data"})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "supermajority"
  extra_data["has_majority"] = False
  extra_data["has_supermajority"] = False
  extra_data["danger_client"] = ""
  if sorted_data[0]["value"] >= .50:
    extra_data["has_majority"] = True
    extra_data["danger_client"] = sorted_data[0]["name"]
  if sorted_data[0]["value"] >= .66:
    extra_data["has_supermajority"] = True
  extra_data["top_client"] = sorted_data[0]["name"]
  extra_data["validators_represented"] = sample_size
  extra_data["validators_total"] = total_validators
  validators_percentage = sample_size / total_validators
  extra_data["validators_percentage"] = validators_percentage
  # pprint(["extra_data", extra_data])

  # create final data dict
  final_data["distribution"] = sorted_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_supermajority")

  return final_data

def supermajority_marketshare():
  raw_data = get_supermajority_marketshare_data()
  save_to_file("../_data/raw/supermajority_raw.json", raw_data)
  raw_total_validators = get_supermajority_total_validators()
  total_validators = process_supermajority_total_validators(raw_total_validators)
  processed_data = process_supermajority_marketshare_data(raw_data, total_validators)
  save_to_file("../_data/supermajority.json", processed_data)


########################################
# ETHERNODES
########################################


def get_ethernodes_marketshare_data():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': [{'client': 'geth', 'value': 2508}, {'client': 'nethermind', 'value': 1199}, {'client': 'erigon', 'value': 699}, {'client': 'besu', 'value': 596}, {'client': 'reth', 'value': 9}, {'client': 'teth', 'value': 3}]}
    print_data("fetch", response)
    return response
  else:
    url = "https://ethernodes.org/api/clients"
    response = fetch(url)
    return response

def process_ethernodes_marketshare_data(raw_data):
  # example ethernodes raw data:
  # raw_data = {'status': 200, 'attempts': 1, 'data': [
  #   {'client': 'geth', 'value': 2508}, 
  #   {'client': 'nethermind', 'value': 1199}, 
  #   {'client': 'erigon', 'value': 699}, 
  #   {'client': 'besu', 'value': 596}, 
  #   {'client': 'reth', 'value': 9}, 
  #   {'client': 'teth', 'value': 3}
  #   ]}

  main_clients = ["geth", "erigon", "nethermind", "besu", "reth"]
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  sample_size = 0
  reformatted_data = []
  filtered_data = [{"name": "other", "value": 0}]
  marketshare_data = []
  extra_data = {}
  final_data = {}

  # reformat data into a list of dicts
  for item in raw_data["data"]:
    reformatted_data.append({"name": item["client"].lower(), "value": item["value"]})
    sample_size += item["value"]
  # pprint(["reformatted_data", reformatted_data])
  # pprint(["sample_size", sample_size])

  # filter out items either under the threshold and not in the main_clients list
  for item in reformatted_data:
    if item["name"] in main_clients:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    elif (item["value"] / sample_size * 100) >= threshold_percentage:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    else:
      filtered_data[0]["value"] += item["value"]
  # pprint(["filtered_data", filtered_data])

  # calculate the marketshare for each client
  for item in filtered_data:
    marketshare = item["value"] / sample_size
    marketshare_data.append({"name": item["name"], "value": marketshare, "accuracy": "no data"})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "ethernodes"
  extra_data["has_majority"] = False
  extra_data["has_supermajority"] = False
  extra_data["danger_client"] = ""
  if sorted_data[0]["value"] >= .50:
    extra_data["has_majority"] = True
    extra_data["danger_client"] = sorted_data[0]["name"]
  if sorted_data[0]["value"] >= .66:
    extra_data["has_supermajority"] = True
  extra_data["top_client"] = sorted_data[0]["name"]
  # pprint(["extra_data", extra_data])

  # create final data dict
  final_data["distribution"] = sorted_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_ethernodes")

  return final_data

def ethernodes_marketshare():
  raw_data = get_ethernodes_marketshare_data()
  save_to_file("../_data/raw/ethernodes_raw.json", raw_data)
  processed_data = process_ethernodes_marketshare_data(raw_data)
  save_to_file("../_data/ethernodes.json", processed_data)


########################################
# MIGALABS
########################################


def get_migalabs_marketshare_data():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': [{"timestamp":"2023-10-03T04:37:09Z","data":[{"client_name":"lighthouse","node_count":2867},{"client_name":"prysm","node_count":2206},{"client_name":"teku","node_count":1303},{"client_name":"nimbus","node_count":836},{"client_name":"lodestar","node_count":252},{"client_name":"grandine","node_count":213},{"client_name":"unknown","node_count":28}]}]}
    print_data("fetch", response)
    return response
  else:
    url = "https://www.migalabs.io/api/eth/v1/nodes/consensus/all/client_diversity"
    payload = {}
    headers = {
      'X-Api-Key': migalabs_token
    }
    response = fetch(url, "GET", payload, headers)
    return response

def process_migalabs_marketshare_data(raw_data):
  # example migalabs raw data:
    # raw_data = {'status': 200, 'attempts': 1, 'data': [{
    #   "timestamp": "2023-10-03T04:37:09Z",
    #   "data": [
    #     {
    #       "client_name": "lighthouse",
    #       "node_count": 2867
    #     },
    #     {
    #       "client_name": "prysm",
    #       "node_count": 2206
    #     },
    #     {
    #       "client_name": "teku",
    #       "node_count": 1303
    #     },
    #     {
    #       "client_name": "nimbus",
    #       "node_count": 836
    #     },
    #     {
    #       "client_name": "lodestar",
    #       "node_count": 252
    #     },
    #     {
    #       "client_name": "grandine",
    #       "node_count": 213
    #     },
    #     {
    #       "client_name": "unknown",
    #       "node_count": 28
    #     }
    #   ]
    # }]}

  main_clients = ["lighthouse", "nimbus", "teku", "prysm", "lodestar", "erigon", "grandine"]
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  sample_size = 0
  reformatted_data = []
  filtered_data = [{"name": "other", "value": 0}]
  marketshare_data = []
  extra_data = {}
  final_data = {}

  # reformat data into a list of dicts
  for item in raw_data["data"][0]["data"]:
    reformatted_data.append({"name": item["client_name"].lower(), "value": item["node_count"]})
    sample_size += item["node_count"]
  # pprint(["reformatted_data", reformatted_data])
  # pprint(["sample_size", sample_size])

  # filter out items either under the threshold and not in the main_clients list
  for item in reformatted_data:
    if item["name"] in main_clients:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    elif (item["value"] / sample_size * 100) >= threshold_percentage:
      filtered_data.append({"name": item["name"], "value": item["value"]})
    else:
      filtered_data[0]["value"] += item["value"]
  # pprint(["filtered_data", filtered_data])

  # calculate the marketshare for each client
  for item in filtered_data:
    marketshare = item["value"] / sample_size
    marketshare_data.append({"name": item["name"], "value": marketshare, "accuracy": "no data"})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "migalabs"
  extra_data["has_majority"] = False
  extra_data["has_supermajority"] = False
  extra_data["danger_client"] = ""
  if sorted_data[0]["value"] >= .50:
    extra_data["has_majority"] = True
    extra_data["danger_client"] = sorted_data[0]["name"]
  if sorted_data[0]["value"] >= .66:
    extra_data["has_supermajority"] = True
  extra_data["top_client"] = sorted_data[0]["name"]
  # pprint(["extra_data", extra_data])

  # create final data dict
  final_data["distribution"] = sorted_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_migalabs")

  return final_data

def migalabs_marketshare():
  raw_data = get_migalabs_marketshare_data()
  save_to_file("../_data/raw/migalabs_raw.json", raw_data["data"])
  processed_data = process_migalabs_marketshare_data(raw_data)
  save_to_file("../_data/migalabs.json", processed_data)


########################################


def get_data():
  if day == "Saturday" or current_time < 1747032025:
    rated_marketshare()
  supermajority_marketshare()
  ethernodes_marketshare()
  migalabs_marketshare()


get_data()



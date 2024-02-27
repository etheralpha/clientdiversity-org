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
migalabs_token = os.environ.get("MIGALABS_API_KEY")
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



def get_rated_overview_data():
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

def process_rated_overview_data(raw_data):
  # get the validator count
  validator_count = raw_data["data"][0]["validatorCount"]
  print_data("processed", validator_count, "validator_count")
  return validator_count


def get_rated_operator_pool_data():
  if use_test_data:
    # response split into multiple lines so it can be collapsed
    response = {'status': 200, 'attempts': 1, 'data': 

      {'page': {'from': None, 'to': None, 'size': 100, 'granularity': None, 'filterType': None}, 'total': 31, 'data': [{'id': 'Lido', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 234187, 'avgCorrectness': 0.993726633441454, 'avgInclusionDelay': 1.022812108183317, 'avgUptime': 0.9988873921094028, 'avgValidatorEffectiveness': 97.12750897959496, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.37956359121125394}, {'client': 'Lodestar', 'percentage': 0.033033510501370406}, {'client': 'Nimbus', 'percentage': 0.03896182558791018}, {'client': 'Prysm', 'percentage': 0.3298051151592241}, {'client': 'Teku', 'percentage': 0.21863595754024137}], 'networkPenetration': 0.3215798659506014, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.1937044378002486}, {'relayer': 'manifold', 'percentage': 0.001310175697920516}, {'relayer': 'blocknative', 'percentage': 0.08862162797729028}, {'relayer': 'no_mev_boost', 'percentage': 0.018779185003527397}, {'relayer': 'bloxroute_regulated', 'percentage': 0.15198038095877986}, {'relayer': 'agnostic', 'percentage': 0.1553398058252427}, {'relayer': 'aestus', 'percentage': 0.04538582994591326}, {'relayer': 'edennetwork', 'percentage': 0.01404239594181476}, {'relayer': 'flashbots', 'percentage': 0.12164477441462021}, {'relayer': 'ultra_sound_money', 'percentage': 0.20915779218597777}, {'relayer': 'bloxroute_ethical', 'percentage': 3.359424866462861e-05}], 'nodeOperatorCount': 30, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Lido', 'aprPercentage': 4.59}, {'id': 'Coinbase', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 73434, 'avgCorrectness': 0.9948444204225114, 'avgInclusionDelay': 1.0202507882094498, 'avgUptime': 0.9982809511129033, 'avgValidatorEffectiveness': 97.3930362697948, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.3966019520700874}, {'client': 'Nimbus', 'percentage': 0.035681629702086035}, {'client': 'Prysm', 'percentage': 0.3422501966955153}, {'client': 'Teku', 'percentage': 0.22546622153231122}], 'networkPenetration': 0.10083777441197189, 'relayerPercentages': [{'relayer': 'ultra_sound_money', 'percentage': 0.24420383664822878}, {'relayer': 'blocknative', 'percentage': 0.013298811345180652}, {'relayer': 'aestus', 'percentage': 0.0024714605154760503}, {'relayer': 'no_mev_boost', 'percentage': 0.010591973637754501}, {'relayer': 'agnostic', 'percentage': 0.20760268329998824}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.36471695892668}, {'relayer': 'bloxroute_regulated', 'percentage': 0.040131811227492056}, {'relayer': 'flashbots', 'percentage': 0.11627633282334941}, {'relayer': 'manifold', 'percentage': 0.00023537719195010004}, {'relayer': 'edennetwork', 'percentage': 0.0004707543839002001}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Coinbase', 'aprPercentage': 4.66}, {'id': 'Binance', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 41098, 'avgCorrectness': 0.9941272520338371, 'avgInclusionDelay': 1.0206046662702684, 'avgUptime': 0.9992489805629131, 'avgValidatorEffectiveness': 97.3858552000696, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.612957769712966}, {'client': 'Nimbus', 'percentage': 0.00024744308808973936}, {'client': 'Prysm', 'percentage': 0.386052457934675}, {'client': 'Teku', 'percentage': 0.0007423292642692181}], 'networkPenetration': 0.05643476935456629, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.03450465707027942}, {'relayer': 'blocknative', 'percentage': 0.06604572396274344}, {'relayer': 'agnostic', 'percentage': 0.04403048264182896}, {'relayer': 'ultra_sound_money', 'percentage': 0.29106689246401357}, {'relayer': 'bloxroute_regulated', 'percentage': 0.24174428450465707}, {'relayer': 'no_mev_boost', 'percentage': 0.006985605419136325}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.12235393734123624}, {'relayer': 'flashbots', 'percentage': 0.193268416596105}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Binance', 'aprPercentage': 4.72}, {'id': 'Kraken', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 24561, 'avgCorrectness': 0.9949079416133426, 'avgInclusionDelay': 1.0209231973227801, 'avgUptime': 0.9987906142765821, 'avgValidatorEffectiveness': 97.38967836162888, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.02180460185519817}, {'client': 'Nimbus', 'percentage': 0.00030116853391157694}, {'client': 'Prysm', 'percentage': 0.9413323695940248}, {'client': 'Teku', 'percentage': 0.03656186001686544}], 'networkPenetration': 0.033285775686278815, 'relayerPercentages': [{'relayer': 'blocknative', 'percentage': 0.05123398937831927}, {'relayer': 'aestus', 'percentage': 0.030927835051546393}, {'relayer': 'ultra_sound_money', 'percentage': 0.1836925960637301}, {'relayer': 'edennetwork', 'percentage': 0.010621680724773508}, {'relayer': 'flashbots', 'percentage': 0.32146204311152765}, {'relayer': 'no_mev_boost', 'percentage': 0.016869728209934397}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.1543267728834739}, {'relayer': 'agnostic', 'percentage': 0.22992814745392065}, {'relayer': 'manifold', 'percentage': 0.0009372071227741331}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Kraken', 'aprPercentage': 4.58}, {'id': 'Rocketpool', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 22256, 'avgCorrectness': 0.9927764902413493, 'avgInclusionDelay': 1.0271212800957081, 'avgUptime': 0.9830124807085743, 'avgValidatorEffectiveness': 95.14506199159602, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.41736339836162484}, {'client': 'Lodestar', 'percentage': 0.0029558314331559836}, {'client': 'Nimbus', 'percentage': 0.16848239168989107}, {'client': 'Prysm', 'percentage': 0.09610674774090026}, {'client': 'Teku', 'percentage': 0.3150916307744278}], 'networkPenetration': 0.03056139536608174, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.03410024650780608}, {'relayer': 'aestus', 'percentage': 0.0447822514379622}, {'relayer': 'bloxroute_ethical', 'percentage': 0.0045193097781429745}, {'relayer': 'bloxroute_regulated', 'percentage': 0.18323746918652423}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.1914543960558751}, {'relayer': 'flashbots', 'percentage': 0.16803615447822515}, {'relayer': 'ultra_sound_money', 'percentage': 0.18734593262119967}, {'relayer': 'blocknative', 'percentage': 0.1314708299096138}, {'relayer': 'no_mev_boost', 'percentage': 0.03327855382087099}, {'relayer': 'edennetwork', 'percentage': 0.021774856203779787}], 'nodeOperatorCount': 2118, 'operatorTags': [
      {'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Rocketpool', 'aprPercentage': 4.48}, {'id': 'Bitcoin Suisse', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 13725, 'avgCorrectness': 0.9934730782222934, 'avgInclusionDelay': 1.0227518067626231, 'avgUptime': 0.9992559053979818, 'avgValidatorEffectiveness': 97.12659904050217, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0002257336343115124}, {'client': 'Nimbus', 'percentage': 0.02528216704288939}, {'client': 'Prysm', 'percentage': 0.0012415349887133183}, {'client': 'Teku', 'percentage': 0.9732505643340857}], 'networkPenetration': 0.018846834624347227, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.15445232466509062}, {'relayer': 'ultra_sound_money', 'percentage': 0.16233254531126873}, {'relayer': 'edennetwork', 'percentage': 0.03664302600472813}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.2470449172576832}, {'relayer': 'bloxroute_regulated', 'percentage': 0.24152876280535854}, {'relayer': 'blocknative', 'percentage': 0.15642237982663515}, {'relayer': 'manifold', 'percentage': 0.0007880220646178094}, {'relayer': 'no_mev_boost', 'percentage': 0.0003940110323089047}, {'relayer': 'bloxroute_ethical', 'percentage': 0.0003940110323089047}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'custodian', 'path': None, 'idType': None}], 'displayName': 'Bitcoin Suisse', 'aprPercentage': 4.35}, {'id': 'Celsius Network', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 11146, 'avgCorrectness': 0.9956812266178313, 'avgInclusionDelay': 1.0234562032588206, 'avgUptime': 0.999289716006027, 'avgValidatorEffectiveness': 97.28277002636149, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0019646365422396855}, {'client': 'Nimbus', 'percentage': 0.0004365858982754857}, {'client': 'Prysm', 'percentage': 0.9965073128137961}, {'client': 'Teku', 'percentage': 0.0010914647456887142}], 'networkPenetration': 0.015305414843203947, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.018891687657430732}, {'relayer': 'flashbots', 'percentage': 0.9811083123425692}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Celsius Network', 'aprPercentage': 4.73}, {'id': 'Whale 0x5d76a', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 10603, 'avgCorrectness': 0.9954162547997246, 'avgInclusionDelay': 1.0190107360282337, 'avgUptime': 0.9999179028397173, 'avgValidatorEffectiveness': 97.72139614757302, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.01572052401746725}, {'client': 'Nimbus', 'percentage': 0.20058224163027658}, {'client': 'Prysm', 'percentage': 0.20844250363901018}, {'client': 'Teku', 'percentage': 0.575254730713246}], 'networkPenetration': 0.014559780511617751, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.0036798528058877645}, {'relayer': 'flashbots', 'percentage': 0.13615455381784727}, {'relayer': 'blocknative', 'percentage': 0.08187672493100276}, {'relayer': 'aestus', 'percentage': 0.09199632014719411}, {'relayer': 'ultra_sound_money', 'percentage': 0.17479300827966882}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.31922723091076355}, {'relayer': 'agnostic', 'percentage': 0.1922723091076357}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Whale 0x5d76a', 'aprPercentage': 4.64}, {'id': 'OKex', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 8331, 'avgCorrectness': 0.9943389739654295, 'avgInclusionDelay': 1.0196420801692967, 'avgUptime': 0.9998473988890638, 'avgValidatorEffectiveness': 97.55284068634985, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.00325821341297855}, {'client': 'Nimbus', 'percentage': 0.00027151778441487917}, {'client': 'Prysm', 'percentage': 0.9937550909584578}, {'client': 'Teku', 'percentage': 0.0027151778441487917}], 'networkPenetration': 0.01143992562881142, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.21678321678321677}, {'relayer': 'edennetwork', 'percentage': 0.03496503496503497}, {'relayer': 'ultra_sound_money', 'percentage': 0.13986013986013987}, {'relayer': 'blocknative', 'percentage': 0.12878787878787878}, {'relayer': 'flashbots', 'percentage': 0.11130536130536131}, {'relayer': 'bloxroute_regulated', 'percentage': 0.2191142191142191}, {'relayer': 'agnostic', 'percentage': 0.1486013986013986}, {'relayer': 'no_mev_boost', 'percentage': 0.0005827505827505828}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'OKex', 'aprPercentage': 4.67}, {'id': 'Ledger Live', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 7937, 'avgCorrectness': 0.9944569951463684, 'avgInclusionDelay': 1.020500085486865, 'avgUptime': 0.9998419963885397, 'avgValidatorEffectiveness': 97.48560668465123, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.4404320987654321}, {'client': 'Prysm', 'percentage': 0.558641975308642}, {'client': 'Teku', 'percentage': 0.000925925925925926}], 'networkPenetration': 0.010898894456352929, 'relayerPercentages': [{'relayer': 'manifold', 'percentage': 0.0006544502617801048}, {'relayer': 'blocknative', 'percentage': 0.09096858638743456}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.2212041884816754}, {'relayer': 'bloxroute_regulated', 'percentage': 0.2205497382198953}, {'relayer': 'agnostic', 'percentage': 0.14136125654450263}, {'relayer': 'ultra_sound_money', 'percentage': 0.17539267015706805}, {'relayer': 'edennetwork', 'percentage': 0.01832460732984293}, {'relayer': 'flashbots', 'percentage': 0.09424083769633508}, {'relayer': 'aestus', 'percentage': 0.03599476439790576}, {'relayer': 'no_mev_boost', 'percentage': 0.0013089005235602095}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'wallet', 'path': None, 'idType': None}], 'displayName': 'Ledger Live', 'aprPercentage': 4.55}, {'id': 'Frax', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 6168, 'avgCorrectness': 0.9958481017047883, 'avgInclusionDelay': 1.0195834230392993, 'avgUptime': 0.9998665298063167, 'avgValidatorEffectiveness': 97.70596901220054, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.5743181121667178}, {'client': 'Nimbus', 'percentage': 0.0009193993257738277}, {'client': 'Prysm', 'percentage': 0.4238430891817346}, {'client': 'Teku', 'percentage': 0.0009193993257738277}], 'networkPenetration': 0.008469746882548174, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.015283842794759825}, {'relayer': 'flashbots', 'percentage': 0.1517467248908297}, {'relayer': 'no_mev_boost', 'percentage': 0.007641921397379912}, {'relayer': 'agnostic', 'percentage': 0.4421397379912664}, {'relayer': 'ultra_sound_money', 'percentage': 0.38318777292576417}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Frax', 'aprPercentage': 4.82}, {'id': 'Wedex', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 3748, 'avgCorrectness': 0.9925165980726773, 'avgInclusionDelay': 1.0221779320624513, 'avgUptime': 0.9992166827599056, 'avgValidatorEffectiveness': 97.08032765692879, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.9966344131257888}, {'client': 'Nimbus', 'percentage': 0.0033655868742111907}], 'networkPenetration': 0.005146662016178754, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.21146245059288538}, {'relayer': 'blocknative', 'percentage': 0.0533596837944664}, {'relayer': 'flashbots', 'percentage': 0.07509881422924901}, {'relayer': 'no_mev_boost', 'percentage': 0.06521739130434782}, {'relayer': 'aestus', 'percentage': 0.01383399209486166}, {'relayer': 'ultra_sound_money', 'percentage': 0.2490118577075099}, {'relayer': 'agnostic', 'percentage': 0.3201581027667984}, {'relayer': 'edennetwork', 'percentage': 0.003952569169960474}, {'relayer': 'manifold', 'percentage': 0.007905138339920948}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Wedex', 'aprPercentage': 4.6}, {'id': 'Bitfinex', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 3373, 'avgCorrectness': 0.9921892630536591, 'avgInclusionDelay': 1.0272304908539234, 'avgUptime': 0.9989955717438671, 'avgValidatorEffectiveness': 96.5825094367404, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0018475750577367205}, {'client': 'Prysm', 'percentage': 0.9958429561200923}, {'client': 'Teku', 'percentage': 0.0023094688221709007}], 'networkPenetration': 0.004631721179447956, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.007722007722007722}, {'relayer': 'edennetwork', 'percentage': 0.003861003861003861}, {'relayer': 'no_mev_boost', 'percentage': 0.0694980694980695}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.04247104247104247}, {'relayer': 'agnostic', 'percentage': 0.02702702702702703}, {'relayer': 'flashbots', 'percentage': 0.7953667953667953}, {'relayer': 'ultra_sound_money', 'percentage': 0.03088803088803089}, {'relayer': 'blocknative', 'percentage': 0.023166023166023165}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Bitfinex', 'aprPercentage': 4.32}, {'id': 'StakeWise', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 2527, 'avgCorrectness': 0.9920072116347213, 'avgInclusionDelay': 1.0256374524814358, 'avgUptime': 0.9981566996139897, 'avgValidatorEffectiveness': 96.69471795229425, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.4250783699059561}, {'client': 'Nimbus', 'percentage': 0.015047021943573668}, {'client': 'Teku', 'percentage': 0.5598746081504702}], 'networkPenetration': 0.0034700146517832745, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.015037593984962405}, {'relayer': 'flashbots', 'percentage': 0.10902255639097744}, {'relayer': 'aestus', 'percentage': 0.03007518796992481}, {'relayer': 'agnostic', 'percentage': 0.3383458646616541}, {'relayer': 'ultra_sound_money', 'percentage': 0.23684210526315788}, {'relayer': 'no_mev_boost', 'percentage': 0.07142857142857142}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.09022556390977443}, {'relayer': 'blocknative', 'percentage': 0.10902255639097744}], 'nodeOperatorCount': 5, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'StakeWise', 'aprPercentage': 4.36}, {'id': 'StakeHound', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 1944, 'avgCorrectness': 0.9960434695745096, 'avgInclusionDelay': 1.0189132824123295, 'avgUptime': 0.9999363119733491, 'avgValidatorEffectiveness': 97.78297460142377, 'clientPercentages': [
      {'client': 'Nimbus', 'percentage': 0.025179856115107913}, {'client': 'Teku', 'percentage': 0.9748201438848921}], 'networkPenetration': 0.0026694532976124594, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.14473684210526316}, {'relayer': 'bloxroute_regulated', 'percentage': 0.22894736842105262}, {'relayer': 'aestus', 'percentage': 0.060526315789473685}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.21842105263157896}, {'relayer': 'agnostic', 'percentage': 0.15526315789473685}, {'relayer': 'edennetwork', 'percentage': 0.031578947368421054}, {'relayer': 'ultra_sound_money', 'percentage': 0.15789473684210525}, {'relayer': 'no_mev_boost', 'percentage': 0.002631578947368421}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'StakeHound', 'aprPercentage': 5.04}, {'id': 'Bitstamp', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 1924, 'avgCorrectness': 0.9940955477530529, 'avgInclusionDelay': 1.0208576706214647, 'avgUptime': 0.999556346421047, 'avgValidatorEffectiveness': 97.39111179379319, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0022371364653243847}, {'client': 'Prysm', 'percentage': 0.9962714392244594}, {'client': 'Teku', 'percentage': 0.0014914243102162564}], 'networkPenetration': 0.0026419897863201505, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.0223463687150838}, {'relayer': 'no_mev_boost', 'percentage': 0.013966480446927373}, {'relayer': 'aestus', 'percentage': 0.04189944134078212}, {'relayer': 'agnostic', 'percentage': 0.2709497206703911}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.20949720670391062}, {'relayer': 'ultra_sound_money', 'percentage': 0.22346368715083798}, {'relayer': 'blocknative', 'percentage': 0.10335195530726257}, {'relayer': 'flashbots', 'percentage': 0.11173184357541899}, {'relayer': 'manifold', 'percentage': 0.002793296089385475}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Bitstamp', 'aprPercentage': 5.85}, {'id': 'Huobi', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 1458, 'avgCorrectness': 0.9953170687839411, 'avgInclusionDelay': 1.0214802964666196, 'avgUptime': 0.9996390783458224, 'avgValidatorEffectiveness': 97.46528010550327, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.001638001638001638}, {'client': 'Prysm', 'percentage': 0.9975429975429976}, {'client': 'Teku', 'percentage': 0.000819000819000819}], 'networkPenetration': 0.0019718801107878044, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.02631578947368421}, {'relayer': 'blocknative', 'percentage': 0.12105263157894737}, {'relayer': 'bloxroute_regulated', 'percentage': 0.30526315789473685}, {'relayer': 'agnostic', 'percentage': 0.10526315789473684}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.23157894736842105}, {'relayer': 'flashbots', 'percentage': 0.08947368421052632}, {'relayer': 'ultra_sound_money', 'percentage': 0.12105263157894737}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Huobi', 'aprPercentage': 5.31}, {'id': 'Ankr', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 1327, 'avgCorrectness': 0.9948957478977004, 'avgInclusionDelay': 1.0207924767130718, 'avgUptime': 0.9014231865145435, 'avgValidatorEffectiveness': 87.90894649085247, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.7472527472527473}, {'client': 'Prysm', 'percentage': 0.2509157509157509}, {'client': 'Teku', 'percentage': 0.0018315018315018315}], 'networkPenetration': 0.0018029795163401025, 'relayerPercentages': [{'relayer': 'bloxroute_regulated', 'percentage': 0.13008130081300814}, {'relayer': 'flashbots', 'percentage': 0.11382113821138211}, {'relayer': 'ultra_sound_money', 'percentage': 0.18699186991869918}, {'relayer': 'agnostic', 'percentage': 0.2682926829268293}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.21951219512195122}, {'relayer': 'blocknative', 'percentage': 0.056910569105691054}, {'relayer': 'aestus', 'percentage': 0.024390243902439025}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Ankr', 'aprPercentage': 4.81}, {'id': 'Swell', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 1042, 'avgCorrectness': 0.994062122866175, 'avgInclusionDelay': 1.0210968505264826, 'avgUptime': 0.9990026076811737, 'avgValidatorEffectiveness': 97.30137089586893, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.5768194070080862}, {'client': 'Nimbus', 'percentage': 0.005390835579514825}, {'client': 'Prysm', 'percentage': 0.31805929919137466}, {'client': 'Teku', 'percentage': 0.09973045822102426}], 'networkPenetration': 0.0014308489383293122, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.02702702702702703}, {'relayer': 'blocknative', 'percentage': 0.10135135135135136}, {'relayer': 'bloxroute_regulated', 'percentage': 0.16216216216216217}, {'relayer': 'flashbots', 'percentage': 0.12837837837837837}, {'relayer': 'ultra_sound_money', 'percentage': 0.20945945945945946}, {'relayer': 'aestus', 'percentage': 0.0472972972972973}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.20270270270270271}, {'relayer': 'agnostic', 'percentage': 0.11486486486486487}, {'relayer': 'no_mev_boost', 'percentage': 0.006756756756756757}], 'nodeOperatorCount': 8, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Swell', 'aprPercentage': 4.35}, {'id': 'Kucoin', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 827, 'avgCorrectness': 0.9953127586432561, 'avgInclusionDelay': 1.0192378613306439, 'avgUptime': 0.9971747183355406, 'avgValidatorEffectiveness': 97.42383672142485, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0019120458891013384}, {'client': 'Prysm', 'percentage': 0.9980879541108987}], 'networkPenetration': 0.0011356161919369877, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.15841584158415842}, {'relayer': 'bloxroute_regulated', 'percentage': 0.1485148514851485}, {'relayer': 'no_mev_boost', 'percentage': 0.27722772277227725}, {'relayer': 'ultra_sound_money', 'percentage': 0.13861386138613863}, {'relayer': 'blocknative', 'percentage': 0.0594059405940594}, {'relayer': 'agnostic', 'percentage': 0.13861386138613863}, {'relayer': 'flashbots', 'percentage': 0.06930693069306931}, {'relayer': 'aestus', 'percentage': 0.009900990099009901}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Kucoin', 'aprPercentage': 4.48}, {'id': 'Whale 0xf805c', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 642, 'avgCorrectness': 0.994520218821616, 'avgInclusionDelay': 1.0220362845737097, 'avgUptime': 0.9988785046728973, 'avgValidatorEffectiveness': 97.26131687196829, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.0008815787124831271, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.05714285714285714}, {'relayer': 'no_mev_boost', 'percentage': 0.3142857142857143}, {'relayer': 'blocknative', 'percentage': 0.11428571428571428}, {'relayer': 'ultra_sound_money', 'percentage': 0.17142857142857143}, {'relayer': 'agnostic', 'percentage': 0.11428571428571428}, {'relayer': 'flashbots', 'percentage': 0.08571428571428572}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.12857142857142856}, {'relayer': 'manifold', 'percentage': 0.014285714285714285}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Whale 0xf805c', 'aprPercentage': 4.31}, {'id': 'Ether Capital', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 640, 'avgCorrectness': 0.9953092189598087, 'avgInclusionDelay': 1.0212603959236266, 'avgUptime': 0.9993710317460317, 'avgValidatorEffectiveness': 97.45606525567594, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.9433497536945813}, {'client': 'Nimbus', 'percentage': 0.0049261083743842365}, {'client': 'Teku', 'percentage': 0.05172413793103448}], 'networkPenetration': 0.0008788323613538962, 'relayerPercentages': [{'relayer': 'blocknative', 'percentage': 0.6724137931034483}, {'relayer': 'flashbots', 'percentage': 0.3275862068965517}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Ether Capital', 'aprPercentage': 4.65}, {'id': 'Wexexchange', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 500, 'avgCorrectness': 0.9957615424209793, 'avgInclusionDelay': 1.0183422394701018, 'avgUptime': 0.9999644444444445, 'avgValidatorEffectiveness': 97.81795755152838, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0031847133757961785}, {'client': 'Prysm', 'percentage': 0.9968152866242038}], 'networkPenetration': 0.0006865877823077314, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.03896103896103896}, {'relayer': 'agnostic', 'percentage': 0.19480519480519481}, {'relayer': 'blocknative', 'percentage': 0.14285714285714285}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.23376623376623376}, {'relayer': 'flashbots', 'percentage': 0.11688311688311688}, {'relayer': 'aestus', 'percentage': 0.09090909090909091}, {'relayer': 'ultra_sound_money', 'percentage': 0.18181818181818182}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Wexexchange', 'aprPercentage': 4.37}, {'id': 'Poloniex', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 400, 'avgCorrectness': 0.9955573123115258, 'avgInclusionDelay': 1.018503085170387, 'avgUptime': 0.9999190476190476, 'avgValidatorEffectiveness': 97.78388277551873, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.0005492702258461851, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.024390243902439025}, {'relayer': 'aestus', 'percentage': 0.07317073170731707}, {'relayer': 'flashbots', 'percentage': 0.08536585365853659}, {'relayer': 'blocknative', 'percentage': 0.10975609756097561}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.18292682926829268}, {'relayer': 'agnostic', 'percentage': 0.14634146341463414}, {'relayer': 'ultra_sound_money', 'percentage': 0.14634146341463414}, {'relayer': 'bloxroute_regulated', 'percentage': 0.23170731707317074}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'exchange', 'path': None, 'idType': None}], 'displayName': 'Poloniex', 'aprPercentage': 4.19}, {'id': 'Bitpie', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 363, 'avgCorrectness': 0.9943681321885328, 'avgInclusionDelay': 1.019147067673382, 'avgUptime': 0.9998303380121562, 'avgValidatorEffectiveness': 97.60111146928617, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.009230769230769232}, {'client': 'Prysm', 'percentage': 0.9907692307692307}], 'networkPenetration': 0.000498462729955413, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.9473684210526315}, {'relayer': 'no_mev_boost', 'percentage': 0.05263157894736842}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'wallet', 'path': None, 'idType': None}], 'displayName': 'Bitpie', 'aprPercentage': 7.04}, {'id': 'StaFi', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 277, 'avgCorrectness': 0.9961584967089632, 'avgInclusionDelay': 1.019033437310336, 'avgUptime': 0.9998313117515424, 'avgValidatorEffectiveness': 97.7882141536355, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.05855855855855856}, {'client': 'Prysm', 'percentage': 0.9414414414414415}], 'networkPenetration': 0.00038036963139848317, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.7}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.1}, {'relayer': 'blocknative', 'percentage': 0.1}, {'relayer': 'bloxroute_regulated', 'percentage': 0.05}, {'relayer': 'ultra_sound_money', 'percentage': 0.05}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'StaFi', 'aprPercentage': 4.28}, {'id': 'SharedStake', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 381, 'avgCorrectness': 0.9954268067765, 'avgInclusionDelay': 1.0185000752485416, 'avgUptime': 0.9993059777077634, 'avgValidatorEffectiveness': 97.67835032333734, 'clientPercentages': [{'client': 'Prysm', 'percentage': 0.9968354430379747}, {'client': 'Teku', 'percentage': 0.0031645569620253164}], 'networkPenetration': 0.0003103376776030946, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.17647058823529413}, {'relayer': 'ultra_sound_money', 'percentage': 0.4117647058823529}, {'relayer': 'agnostic', 'percentage': 0.4117647058823529}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'SharedStake', 'aprPercentage': 6.39}, {'id': 'Vitalik Buterin', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 218, 'avgCorrectness': 0.9943320931145032, 'avgInclusionDelay': 1.0207943033456772, 'avgUptime': 0.9996184651230523, 'avgValidatorEffectiveness': 97.4212966186359, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.9927007299270073}, {'client': 'Nimbus', 'percentage': 0.0072992700729927005}], 'networkPenetration': 0.0002993522730861709, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}, {'name': 'legendary', 'path': None, 'idType': None}], 'displayName': 'Vitalik Buterin', 'aprPercentage': 3.64}, {'id': 'Guarda', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 153, 'avgCorrectness': 0.9961027322556218, 'avgInclusionDelay': 1.0182636664883602, 'avgUptime': 0.5973524224504617, 'avgValidatorEffectiveness': 58.471275144606444, 'clientPercentages': [{'client': 'Prysm', 'percentage': 0.9906542056074766}, {'client': 'Teku', 'percentage': 0.009345794392523364}], 'networkPenetration': 0.0002100958613861658, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Guarda', 'aprPercentage': 1.38}, {'id': 'Bifrost', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 13, 'avgCorrectness': 0.9941211913951178, 'avgInclusionDelay': 1.0194440373247349, 'avgUptime': 0.9997069597069598, 'avgValidatorEffectiveness': 97.54026574059093, 'clientPercentages': [{'client': 'Prysm', 'percentage': 1.0}], 'networkPenetration': 1.7851282340001018e-05, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 1.0}], 'nodeOperatorCount': None, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'Bifrost', 'aprPercentage': 4.14}, {'id': 'pSTAKE', 'idType': 'pool', 'timeWindow': '7d', 'validatorCount': 2, 'avgCorrectness': 0.9959775590134434, 'avgInclusionDelay': 1.010161956176564, 'avgUptime': 0.9996825396825397, 'avgValidatorEffectiveness': 98.57697361376248, 'clientPercentages': [{'client': 'Prysm', 'percentage': 1.0}], 'networkPenetration': 2.7463511292309255e-06, 'relayerPercentages': [], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'pool', 'path': None, 'idType': None}], 'displayName': 'pSTAKE', 'aprPercentage': 2.88}], 'next': None}}
    print_data("fetch", response)
    return response
  else:
    url = "https://api.rated.network/v0/eth/operators?window=7d&idType=pool&size=100"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': rated_token
    }
    response = fetch(url, "GET", payload, headers)
    return response

def process_rated_operator_pool_data(raw_data):
  pool_validator_counts = {}
  for pool in raw_data["data"]["data"]:
    pool_validator_counts[pool["id"]] = pool["validatorCount"]
  print_data("processed", pool_validator_counts, "pool_validator_counts")
  return pool_validator_counts


def get_rated_operator_node_data():
  if use_test_data:
    # response split into multiple lines so it can be collapsed
    response = {'status': 200, 'attempts': 1, 'data': {

      'page': {'from': None, 'to': None, 'size': 100, 'granularity': None, 'filterType': None}, 'total': 52, 'data': [{'id': 'Kiln', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 23810, 'avgCorrectness': 0.9949509406954944, 'avgInclusionDelay': 1.017948702586212, 'avgUptime': 0.9998280828900458, 'avgValidatorEffectiveness': 97.76418156450255, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.333947045414694}, {'client': 'Nimbus', 'percentage': 0.0005260389268805891}, {'client': 'Prysm', 'percentage': 0.6386989303875154}, {'client': 'Teku', 'percentage': 0.026827985270910047}], 'networkPenetration': 0.032216076376861795, 'relayerPercentages': [{'relayer': 'blocknative', 'percentage': 0.09717868338557993}, {'relayer': 'edennetwork', 'percentage': 0.012763098969995522}, {'relayer': 'no_mev_boost', 'percentage': 0.0006717420510523958}, {'relayer': 'aestus', 'percentage': 0.025526197939991044}, {'relayer': 'ultra_sound_money', 'percentage': 0.17129422301836095}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.24406627854903717}, {'relayer': 'manifold', 'percentage': 0.001567398119122257}, {'relayer': 'bloxroute_regulated', 'percentage': 0.23510971786833856}, {'relayer': 'agnostic', 'percentage': 0.1334527541424093}, {'relayer': 'flashbots', 'percentage': 0.07836990595611286}], 'nodeOperatorCount': 4, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Kiln', 'aprPercentage': 4.93}, {'id': 'Allnodes', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 21117, 'avgCorrectness': 0.9962860938572455, 'avgInclusionDelay': 1.0169413849840505, 'avgUptime': 0.9999504713630141, 'avgValidatorEffectiveness': 97.99485409837003, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0004269854824935952}, {'client': 'Nimbus', 'percentage': 0.026643894107600343}, {'client': 'Prysm', 'percentage': 0.002049530315969257}, {'client': 'Teku', 'percentage': 0.9708795900939368}], 'networkPenetration': 0.028572317717353655, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.04551724137931035}, {'relayer': 'ultra_sound_money', 'percentage': 0.20379310344827586}, {'relayer': 'agnostic', 'percentage': 0.12}, {'relayer': 'edennetwork', 'percentage': 0.020689655172413793}, {'relayer': 'aestus', 'percentage': 0.04793103448275862}, {'relayer': 'bloxroute_regulated', 'percentage': 0.18586206896551724}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.19379310344827586}, {'relayer': 'flashbots', 'percentage': 0.18241379310344827}], 'nodeOperatorCount': 4, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Allnodes', 'aprPercentage': 4.48}, {'id': 'Staked.us', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 17645, 'avgCorrectness': 0.9839950250785927, 'avgInclusionDelay': 1.0832035078037132, 'avgUptime': 0.9851717800833385, 'avgValidatorEffectiveness': 91.88462421092014, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.1858641309675522}, {'client': 'Nimbus', 'percentage': 9.802960494069208e-05}, {'client': 'Prysm', 'percentage': 0.6133712381139104}, {'client': 'Teku', 'percentage': 0.2006666013135967}], 'networkPenetration': 0.02387453455143748, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.022641509433962263}, {'relayer': 'no_mev_boost', 'percentage': 0.007127882599580713}, {'relayer': 'ultra_sound_money', 'percentage': 0.2381551362683438}, {'relayer': 'blocknative', 'percentage': 0.1039832285115304}, {'relayer': 'edennetwork', 'percentage': 0.011320754716981131}, {'relayer': 'flashbots', 'percentage': 0.11614255765199162}, {'relayer': 'bloxroute_regulated', 'percentage': 0.06373165618448637}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.2020964360587002}, {'relayer': 'agnostic', 'percentage': 0.23438155136268343}, {'relayer': 'manifold', 'percentage': 0.0004192872117400419}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Staked.us', 'aprPercentage': 5.2}, {'id': 'Stakefish', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 16633, 'avgCorrectness': 0.994058180326725, 'avgInclusionDelay': 1.018652061823221, 'avgUptime': 0.9994040507917248, 'avgValidatorEffectiveness': 97.57234262980086, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.655275723246887}, {'client': 'Nimbus', 'percentage': 0.008613425709203258}, {'client': 'Prysm', 'percentage': 0.0006553693474393783}, {'client': 'Teku', 'percentage': 0.3354554816964704}], 'networkPenetration': 0.022263054208520955, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.16356673960612692}, {'relayer': 'edennetwork', 'percentage': 0.0032822757111597373}, {'relayer': 'flashbots', 'percentage': 0.10722100656455143}, {'relayer': 'ultra_sound_money', 'percentage': 0.17778993435448578}, {'relayer': 'blocknative', 'percentage': 0.06455142231947483}, {'relayer': 'bloxroute_regulated', 'percentage': 0.21936542669584244}, {'relayer': 'no_mev_boost', 'percentage': 0.01312910284463895}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.2510940919037199}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Stakefish', 'aprPercentage': 4.77}, 
      {'id': 'P2P.ORG - P2P Validator', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 13391, 'avgCorrectness': 0.9958846649369913, 'avgInclusionDelay': 1.0177862397361765, 'avgUptime': 0.9998770035723393, 'avgValidatorEffectiveness': 97.87750364727192, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.25857486394127327}, {'client': 'Nimbus', 'percentage': 0.014808252119984811}, {'client': 'Prysm', 'percentage': 0.20275914441209975}, {'client': 'Teku', 'percentage': 0.5238577395266422}], 'networkPenetration': 0.01811866773467267, 'relayerPercentages': [{'relayer': 'bloxroute_regulated', 'percentage': 0.20491803278688525}, {'relayer': 'ultra_sound_money', 'percentage': 0.1828499369482976}, {'relayer': 'agnostic', 'percentage': 0.23203026481715006}, {'relayer': 'flashbots', 'percentage': 0.08007566204287515}, {'relayer': 'edennetwork', 'percentage': 0.0018915510718789407}, {'relayer': 'aestus', 'percentage': 0.03972257250945776}, {'relayer': 'blocknative', 'percentage': 0.02395964691046658}, {'relayer': 'no_mev_boost', 'percentage': 0.0025220680958385876}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.22887767969735182}, {'relayer': 'manifold', 'percentage': 0.0031525851197982345}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'P2P.ORG - P2P Validator', 'aprPercentage': 4.9}, {'id': 'InfStones', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 10040, 'avgCorrectness': 0.9946845322821294, 'avgInclusionDelay': 1.0169943927890641, 'avgUptime': 0.9995934803185333, 'avgValidatorEffectiveness': 97.80254372105335, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0012313104661389623}, {'client': 'Prysm', 'percentage': 0.9978891820580474}, {'client': 'Teku', 'percentage': 0.0008795074758135445}], 'networkPenetration': 0.013584603394527191, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.0858806404657933}, {'relayer': 'no_mev_boost', 'percentage': 0.08151382823871907}, {'relayer': 'agnostic', 'percentage': 0.15211062590975255}, {'relayer': 'bloxroute_regulated', 'percentage': 0.18922852983988356}, {'relayer': 'edennetwork', 'percentage': 0.011644832605531296}, {'relayer': 'blocknative', 'percentage': 0.01455604075691412}, {'relayer': 'aestus', 'percentage': 0.029839883551673944}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.23871906841339155}, {'relayer': 'manifold', 'percentage': 0.002911208151382824}, {'relayer': 'ultra_sound_money', 'percentage': 0.19359534206695778}], 'nodeOperatorCount': 3, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'InfStones', 'aprPercentage': 4.31}, {'id': 'Chorus One', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 9133, 'avgCorrectness': 0.9957167960152612, 'avgInclusionDelay': 1.0181790652773917, 'avgUptime': 0.9996925146456918, 'avgValidatorEffectiveness': 97.80409987138766, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.999198717948718}, {'client': 'Teku', 'percentage': 0.0008012820512820513}], 'networkPenetration': 0.012357388725320401, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.17647058823529413}, {'relayer': 'blocknative', 'percentage': 0.1607843137254902}, {'relayer': 'agnostic', 'percentage': 0.2679738562091503}, {'relayer': 'edennetwork', 'percentage': 0.013071895424836602}, {'relayer': 'ultra_sound_money', 'percentage': 0.37516339869281046}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.00522875816993464}, {'relayer': 'no_mev_boost', 'percentage': 0.00130718954248366}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Chorus One', 'aprPercentage': 4.34}, {'id': 'CryptoManufaktur', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 9089, 'avgCorrectness': 0.9927518070477906, 'avgInclusionDelay': 1.0228105817011528, 'avgUptime': 0.9980663214827067, 'avgValidatorEffectiveness': 96.95081621430828, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.23091020158827122}, {'client': 'Nimbus', 'percentage': 0.06760333944206882}, {'client': 'Prysm', 'percentage': 0.003868865811443698}, {'client': 'Teku', 'percentage': 0.6976175931582163}], 'networkPenetration': 0.01229785460685833, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.006793478260869565}, {'relayer': 'no_mev_boost', 'percentage': 0.010869565217391304}, {'relayer': 'ultra_sound_money', 'percentage': 0.25679347826086957}, {'relayer': 'flashbots', 'percentage': 0.13043478260869565}, {'relayer': 'agnostic', 'percentage': 0.012228260869565218}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.4578804347826087}, {'relayer': 'aestus', 'percentage': 0.010869565217391304}, {'relayer': 'blocknative', 'percentage': 0.11413043478260869}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'CryptoManufaktur', 'aprPercentage': 4.63}, {'id': 'RockX', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8906, 'avgCorrectness': 0.9958600589508909, 'avgInclusionDelay': 1.0195199858326254, 'avgUptime': 0.9997379603236106, 'avgValidatorEffectiveness': 97.70340844311204, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.045201115093588214}, {'client': 'Nimbus', 'percentage': 0.00019912385503783353}, {'client': 'Prysm', 'percentage': 0.9542015133412983}, {'client': 'Teku', 'percentage': 0.00039824771007566706}], 'networkPenetration': 0.012050246795981987, 'relayerPercentages': [{'relayer': 'blocknative', 'percentage': 0.3310734463276836}, {'relayer': 'edennetwork', 'percentage': 0.05649717514124294}, {'relayer': 'ultra_sound_money', 'percentage': 0.3581920903954802}, {'relayer': 'flashbots', 'percentage': 0.2519774011299435}, {'relayer': 'no_mev_boost', 'percentage': 0.0022598870056497176}], 'nodeOperatorCount': 3, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'RockX', 'aprPercentage': 5.67}, {'id': 'Stakely', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8841, 'avgCorrectness': 0.996062090365428, 'avgInclusionDelay': 1.0170162257276796, 'avgUptime': 0.9995074629298876, 'avgValidatorEffectiveness': 97.92693458535189, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.380672268907563}, {'client': 'Nimbus', 'percentage': 0.026050420168067228}, {'client': 'Prysm', 'percentage': 0.06281512605042017}, {'client': 'Teku', 'percentage': 0.5304621848739496}], 'networkPenetration': 0.011962298666435747, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.047830923248053395}, {'relayer': 'manifold', 'percentage': 0.010567296996662959}, {'relayer': 'bloxroute_regulated', 'percentage': 0.19688542825361513}, {'relayer': 'ultra_sound_money', 'percentage': 0.15739710789766406}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.20022246941045607}, {'relayer': 'flashbots', 'percentage': 0.10789766407119021}, {'relayer': 'blocknative', 'percentage': 0.10734149054505006}, {'relayer': 'edennetwork', 'percentage': 0.02335928809788654}, {'relayer': 'agnostic', 'percentage': 0.14794215795328142}, {'relayer': 'no_mev_boost', 'percentage': 0.0005561735261401557}], 'nodeOperatorCount': 3, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Stakely', 'aprPercentage': 4.49}, {'id': 'Blockscape', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8837, 'avgCorrectness': 0.9935475539934409, 'avgInclusionDelay': 1.0208816215532739, 'avgUptime': 0.9977106291385561, 'avgValidatorEffectiveness': 97.15939097807697, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.3155885897950984}, {'client': 'Nimbus', 'percentage': 0.004017677782241864}, {'client': 'Prysm', 'percentage': 0.6287665729208517}, {'client': 'Teku', 'percentage': 0.051627159501807955}], 'networkPenetration': 0.011956886473848285, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.18379446640316205}, {'relayer': 'no_mev_boost', 'percentage': 0.004940711462450593}, {'relayer': 'aestus', 'percentage': 0.04743083003952569}, {'relayer': 'flashbots', 'percentage': 0.09782608695652174}, {'relayer': 'blocknative', 'percentage': 0.07114624505928854}, {'relayer': 'bloxroute_regulated', 'percentage': 0.17588932806324112}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.20355731225296442}, {'relayer': 'ultra_sound_money', 'percentage': 0.21541501976284586}], 'nodeOperatorCount': 3, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Blockscape', 'aprPercentage': 4.67}, {'id': 'HashQuark', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8836, 'avgCorrectness': 0.9949206389618414, 'avgInclusionDelay': 1.017041544654457, 'avgUptime': 0.9998608457106367, 'avgValidatorEffectiveness': 97.8491555981025, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0025375343624444912}, {'client': 'Prysm', 'percentage': 0.9953478536688518}, {'client': 'Teku', 'percentage': 0.002114611968703743}], 'networkPenetration': 0.01195553342570142, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.18934081346423562}, {'relayer': 'ultra_sound_money', 'percentage': 0.20757363253856942}, {'relayer': 'blocknative', 'percentage': 0.14446002805049088}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.28190743338008417}, {'relayer': 'flashbots', 'percentage': 0.1458625525946704}, {'relayer': 'edennetwork', 'percentage': 0.024544179523141654}, {'relayer': 'no_mev_boost', 'percentage': 0.006311360448807854}], 'nodeOperatorCount': 3, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'HashQuark', 'aprPercentage': 4.89}, {'id': 'DSRV', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8836, 'avgCorrectness': 0.9928789252057733, 'avgInclusionDelay': 1.0239355710374545, 'avgUptime': 0.9989957431346593, 'avgValidatorEffectiveness': 96.93890430703671, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.9058072241069647}, {'client': 'Nimbus', 'percentage': 0.09419277589303532}], 'networkPenetration': 0.01195553342570142, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.0010787486515641855}, {'relayer': 'manifold', 'percentage': 0.0010787486515641855}, {'relayer': 'aestus', 'percentage': 0.02696871628910464}, {'relayer': 'flashbots', 'percentage': 0.0825242718446602}, {'relayer': 'blocknative', 'percentage': 0.07281553398058252}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.20658036677454153}, {'relayer': 'agnostic', 'percentage': 0.21251348435814454}, {'relayer': 'ultra_sound_money', 'percentage': 0.18878101402373246}, {'relayer': 'edennetwork', 'percentage': 0.012944983818770227}, {'relayer': 'bloxroute_regulated', 'percentage': 0.1947141316073355}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'DSRV', 'aprPercentage': 4.57}, {'id': 'Figment', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8708, 'avgCorrectness': 0.9955740206679393, 'avgInclusionDelay': 1.0190380857408192, 'avgUptime': 0.9996670966805541, 'avgValidatorEffectiveness': 97.71107309210294, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.929744335896903}, {'client': 'Nimbus', 'percentage': 0.0031178549158179174}, {'client': 'Teku', 'percentage': 0.06713780918727916}], 'networkPenetration': 0.011782343262902667, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.002797202797202797}, {'relayer': 'flashbots', 'percentage': 0.4251748251748252}, {'relayer': 'blocknative', 'percentage': 0.5720279720279721}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Figment', 'aprPercentage': 4.71}, 
      {'id': 'Stakin', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8689, 'avgCorrectness': 0.9938672503576078, 'avgInclusionDelay': 1.0189147178705689, 'avgUptime': 0.9997436848590799, 'avgValidatorEffectiveness': 97.56509803881151, 'clientPercentages': [{'client': 'Nimbus', 'percentage': 0.022667476219388787}, {'client': 'Prysm', 'percentage': 0.0010119409026512851}, {'client': 'Teku', 'percentage': 0.97632058287796}], 'networkPenetration': 0.011756635348112228, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.016337644656228726}, {'relayer': 'agnostic', 'percentage': 0.33900612661674606}, {'relayer': 'manifold', 'percentage': 0.004765146358066712}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.055820285908781485}, {'relayer': 'bloxroute_regulated', 'percentage': 0.049693669162695714}, {'relayer': 'no_mev_boost', 'percentage': 0.004765146358066712}, {'relayer': 'ultra_sound_money', 'percentage': 0.3281143635125936}, {'relayer': 'flashbots', 'percentage': 0.1415929203539823}, {'relayer': 'blocknative', 'percentage': 0.02859087814840027}, {'relayer': 'aestus', 'percentage': 0.031313818924438394}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Stakin', 'aprPercentage': 5.32}, {'id': 'Everstake', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8689, 'avgCorrectness': 0.9943589885707704, 'avgInclusionDelay': 1.0211055372217654, 'avgUptime': 0.9991016087154804, 'avgValidatorEffectiveness': 97.35801508939767, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0014733740265207324}, {'client': 'Nimbus', 'percentage': 0.0008419280151547042}, {'client': 'Prysm', 'percentage': 0.9960008419280152}, {'client': 'Teku', 'percentage': 0.0016838560303094085}], 'networkPenetration': 0.011756635348112228, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.018488308863512777}, {'relayer': 'ultra_sound_money', 'percentage': 0.1631321370309951}, {'relayer': 'flashbots', 'percentage': 0.10114192495921696}, {'relayer': 'no_mev_boost', 'percentage': 0.002175095160413268}, {'relayer': 'agnostic', 'percentage': 0.15551930396954866}, {'relayer': 'manifold', 'percentage': 0.0016313213703099511}, {'relayer': 'aestus', 'percentage': 0.03588907014681892}, {'relayer': 'bloxroute_regulated', 'percentage': 0.20010875475802067}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.21642196846112016}, {'relayer': 'blocknative', 'percentage': 0.1054921152800435}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Everstake', 'aprPercentage': 5.55}, {'id': 'Simply Staking', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8689, 'avgCorrectness': 0.9912519619610377, 'avgInclusionDelay': 1.0239505183746773, 'avgUptime': 0.9982426651019577, 'avgValidatorEffectiveness': 96.71023913193015, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.3016747933008268}, {'client': 'Nimbus', 'percentage': 0.17129531481874072}, {'client': 'Prysm', 'percentage': 0.5185499258002968}, {'client': 'Teku', 'percentage': 0.00847996608013568}], 'networkPenetration': 0.011756635348112228, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.004243281471004243}, {'relayer': 'aestus', 'percentage': 0.04031117397454031}, {'relayer': 'edennetwork', 'percentage': 0.01272984441301273}, {'relayer': 'bloxroute_regulated', 'percentage': 0.17114568599717114}, {'relayer': 'blocknative', 'percentage': 0.11032531824611033}, {'relayer': 'flashbots', 'percentage': 0.11032531824611033}, {'relayer': 'manifold', 'percentage': 0.0021216407355021216}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.185997171145686}, {'relayer': 'agnostic', 'percentage': 0.18175388967468176}, {'relayer': 'ultra_sound_money', 'percentage': 0.18104667609618105}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Simply Staking', 'aprPercentage': 4.94}, {'id': 'Attestant', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8688, 'avgCorrectness': 0.99618261364101, 'avgInclusionDelay': 1.0163649001773056, 'avgUptime': 0.9999527998560199, 'avgValidatorEffectiveness': 98.0437402422617, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.009888491479065854}, {'client': 'Nimbus', 'percentage': 0.16705238796549549}, {'client': 'Prysm', 'percentage': 0.3208499894803282}, {'client': 'Teku', 'percentage': 0.5022091310751104}], 'networkPenetration': 0.011755282299965362, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.08050436469447139}, {'relayer': 'no_mev_boost', 'percentage': 0.0038797284190106693}, {'relayer': 'blocknative', 'percentage': 0.06789524733268672}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.3006789524733269}, {'relayer': 'bloxroute_regulated', 'percentage': 0.27740058195926287}, {'relayer': 'aestus', 'percentage': 0.03685741998060136}, {'relayer': 'agnostic', 'percentage': 0.12027158098933075}, {'relayer': 'ultra_sound_money', 'percentage': 0.11251212415130941}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Attestant', 'aprPercentage': 4.88}, {'id': 'Kukis Global', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8688, 'avgCorrectness': 0.9960943052296969, 'avgInclusionDelay': 1.0166570024175492, 'avgUptime': 0.9999093270979418, 'avgValidatorEffectiveness': 98.00276580621082, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.9851190476190477}, {'client': 'Nimbus', 'percentage': 0.001488095238095238}, {'client': 'Prysm', 'percentage': 0.013392857142857142}], 'networkPenetration': 0.011755282299965362, 'relayerPercentages': [{'relayer': 'ultra_sound_money', 'percentage': 0.24265644955300128}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.18646232439335889}, {'relayer': 'agnostic', 'percentage': 0.19923371647509577}, {'relayer': 'flashbots', 'percentage': 0.14431673052362706}, {'relayer': 'manifold', 'percentage': 0.005108556832694764}, {'relayer': 'edennetwork', 'percentage': 0.005108556832694764}, {'relayer': 'no_mev_boost', 'percentage': 0.005108556832694764}, {'relayer': 'aestus', 'percentage': 0.09323116219667944}, {'relayer': 'blocknative', 'percentage': 0.11877394636015326}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Kukis Global', 'aprPercentage': 4.6}, {'id': 'Prysmatic Labs', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8688, 'avgCorrectness': 0.9954936038211813, 'avgInclusionDelay': 1.016571774235335, 'avgUptime': 0.9999312501991058, 'avgValidatorEffectiveness': 97.95401079239907, 'clientPercentages': [{'client': 'Prysm', 'percentage': 1.0}], 'networkPenetration': 0.011755282299965362, 'relayerPercentages': [{'relayer': 'ultra_sound_money', 'percentage': 0.4992548435171386}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.4932935916542474}, {'relayer': 'no_mev_boost', 'percentage': 0.004470938897168405}, {'relayer': 'manifold', 'percentage': 0.0029806259314456036}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Prysmatic Labs', 'aprPercentage': 4.71}, {'id': 'Nethermind', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8688, 'avgCorrectness': 0.9948590182915753, 'avgInclusionDelay': 1.0177241936671055, 'avgUptime': 0.9998144081354832, 'avgValidatorEffectiveness': 97.77641298267793, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.31564305585277125}, {'client': 'Nimbus', 'percentage': 0.00042799058420714745}, {'client': 'Prysm', 'percentage': 0.6832869676867109}, {'client': 'Teku', 'percentage': 0.0006419858763107211}], 'networkPenetration': 0.011755282299965362, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.12187088274044795}, {'relayer': 'aestus', 'percentage': 0.021080368906455864}, {'relayer': 'no_mev_boost', 'percentage': 0.002635046113306983}, {'relayer': 'ultra_sound_money', 'percentage': 0.17654808959156784}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.24703557312252963}, {'relayer': 'bloxroute_regulated', 'percentage': 0.2450592885375494}, {'relayer': 'edennetwork', 'percentage': 0.00922266139657444}, {'relayer': 'flashbots', 'percentage': 0.08168642951251646}, {'relayer': 'blocknative', 'percentage': 0.09486166007905138}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Nethermind', 'aprPercentage': 4.39}, {'id': 'Blockdaemon', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8600, 'avgCorrectness': 0.9963515958711777, 'avgInclusionDelay': 1.0189893828373544, 'avgUptime': 0.9996228439747284, 'avgValidatorEffectiveness': 97.79138247996755, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0006491398896462187}, {'client': 'Nimbus', 'percentage': 0.0006491398896462187}, {'client': 'Prysm', 'percentage': 0.9974034404414152}, {'client': 'Teku', 'percentage': 0.0012982797792924375}], 'networkPenetration': 0.011636214063041219, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.3770491803278688}, {'relayer': 'blocknative', 'percentage': 0.03278688524590164}, {'relayer': 'no_mev_boost', 'percentage': 0.006557377049180328}, {'relayer': 'edennetwork', 'percentage': 0.00819672131147541}, {'relayer': 'bloxroute_regulated', 'percentage': 0.5754098360655737}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Blockdaemon', 'aprPercentage': 4.53}, {'id': 'ChainLayer', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8600, 'avgCorrectness': 0.9948749220390432, 'avgInclusionDelay': 1.0180623615724071, 'avgUptime': 0.9998356867176349, 'avgValidatorEffectiveness': 97.74835621844464, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.7317171717171718}, {'client': 'Nimbus', 'percentage': 0.0006060606060606061}, {'client': 'Teku', 'percentage': 0.2676767676767677}], 'networkPenetration': 0.011636214063041219, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.0171606864274571}, {'relayer': 'ultra_sound_money', 'percentage': 0.5288611544461779}, {'relayer': 'blocknative', 'percentage': 0.2917316692667707}, {'relayer': 'flashbots', 'percentage': 0.1622464898595944}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'ChainLayer', 'aprPercentage': 4.45}, {'id': 'Consensys', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8563, 'avgCorrectness': 0.9944057551443066, 'avgInclusionDelay': 1.0217016505729477, 'avgUptime': 0.999439080902239, 'avgValidatorEffectiveness': 97.33514498765409, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.5072649572649572}, {'client': 'Teku', 'percentage': 0.49273504273504276}], 'networkPenetration': 0.011586151281607204, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.009458297506448839}, {'relayer': 'manifold', 'percentage': 0.0034393809114359416}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.25365434221840066}, {'relayer': 'agnostic', 'percentage': 0.13241616509028376}, {'relayer': 'ultra_sound_money', 'percentage': 0.21066208082545143}, {'relayer': 'aestus', 'percentage': 0.018056749785038694}, {'relayer': 'blocknative', 'percentage': 0.07738607050730868}, {'relayer': 'bloxroute_regulated', 'percentage': 0.20808254514187446}, {'relayer': 'flashbots', 'percentage': 0.08684436801375753}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Consensys', 'aprPercentage': 4.87}, 
      {'id': 'Staking Facilities', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8400, 'avgCorrectness': 0.994360242674693, 'avgInclusionDelay': 1.0182986656460584, 'avgUptime': 0.9997052910052909, 'avgValidatorEffectiveness': 97.66347866764276, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.5939516129032258}, {'client': 'Nimbus', 'percentage': 0.31794354838709676}, {'client': 'Prysm', 'percentage': 0.04112903225806452}, {'client': 'Teku', 'percentage': 0.0469758064516129}], 'networkPenetration': 0.011365604433668167, 'relayerPercentages': [{'relayer': 'blocknative', 'percentage': 0.06458333333333334}, {'relayer': 'manifold', 'percentage': 0.004166666666666667}, {'relayer': 'bloxroute_regulated', 'percentage': 0.24375}, {'relayer': 'aestus', 'percentage': 0.027083333333333334}, {'relayer': 'ultra_sound_money', 'percentage': 0.13958333333333334}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.284375}, {'relayer': 'no_mev_boost', 'percentage': 0.00625}, {'relayer': 'flashbots', 'percentage': 0.08333333333333333}, {'relayer': 'agnostic', 'percentage': 0.14583333333333334}, {'relayer': 'edennetwork', 'percentage': 0.0010416666666666667}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Staking Facilities', 'aprPercentage': 7.99}, {'id': 'BridgeTower', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8150, 'avgCorrectness': 0.9924621172569185, 'avgInclusionDelay': 1.0243753303982621, 'avgUptime': 0.9990097575226409, 'avgValidatorEffectiveness': 96.86495904049782, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.011027342396951852, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.3492753623188406}, {'relayer': 'flashbots', 'percentage': 0.06521739130434782}, {'relayer': 'no_mev_boost', 'percentage': 0.04057971014492753}, {'relayer': 'manifold', 'percentage': 0.014492753623188406}, {'relayer': 'ultra_sound_money', 'percentage': 0.4115942028985507}, {'relayer': 'bloxroute_ethical', 'percentage': 0.004347826086956522}, {'relayer': 'agnostic', 'percentage': 0.1144927536231884}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'BridgeTower', 'aprPercentage': 5.06}, {'id': 'Twinstake', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 8004, 'avgCorrectness': 0.9949416039210882, 'avgInclusionDelay': 1.017254663782941, 'avgUptime': 0.9997087170700364, 'avgValidatorEffectiveness': 97.81507111435947, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.41018329938900205}, {'client': 'Nimbus', 'percentage': 0.0006109979633401223}, {'client': 'Prysm', 'percentage': 0.5885947046843177}, {'client': 'Teku', 'percentage': 0.0006109979633401223}], 'networkPenetration': 0.010829797367509525, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.22995031937544358}, {'relayer': 'aestus', 'percentage': 0.0269694819020582}, {'relayer': 'blocknative', 'percentage': 0.10432931156848829}, {'relayer': 'bloxroute_regulated', 'percentage': 0.22782114975159687}, {'relayer': 'flashbots', 'percentage': 0.099361249112846}, {'relayer': 'no_mev_boost', 'percentage': 0.0021291696238466998}, {'relayer': 'agnostic', 'percentage': 0.12207239176721078}, {'relayer': 'ultra_sound_money', 'percentage': 0.18594748048261178}, {'relayer': 'manifold', 'percentage': 0.0014194464158978}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Twinstake', 'aprPercentage': 4.67}, {'id': 'RockLogic GmbH', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 5789, 'avgCorrectness': 0.9669165677145917, 'avgInclusionDelay': 1.0789132648338424, 'avgUptime': 0.9905275193511506, 'avgValidatorEffectiveness': 89.24502097730063, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.24512228634240177}, {'client': 'Nimbus', 'percentage': 0.2044517724649629}, {'client': 'Prysm', 'percentage': 0.13190436933223412}, {'client': 'Teku', 'percentage': 0.41852157186040123}], 'networkPenetration': 0.007832795722202978, 'relayerPercentages': [{'relayer': 'edennetwork', 'percentage': 0.01800450112528132}, {'relayer': 'ultra_sound_money', 'percentage': 0.14103525881470366}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.22580645161290322}, {'relayer': 'blocknative', 'percentage': 0.11477869467366841}, {'relayer': 'manifold', 'percentage': 0.003000750187546887}, {'relayer': 'agnostic', 'percentage': 0.1447861965491373}, {'relayer': 'flashbots', 'percentage': 0.09377344336084022}, {'relayer': 'aestus', 'percentage': 0.0450112528132033}, {'relayer': 'bloxroute_regulated', 'percentage': 0.21380345086271568}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'RockLogic GmbH', 'aprPercentage': 4.63}, {'id': 'Bloxstaking', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 3603, 'avgCorrectness': 0.9945387425509173, 'avgInclusionDelay': 1.0176651243832087, 'avgUptime': 0.9978023717654465, 'avgValidatorEffectiveness': 97.55305862255113, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.4220935841775205}, {'client': 'Lodestar', 'percentage': 0.000964785335262904}, {'client': 'Nimbus', 'percentage': 0.001447178002894356}, {'client': 'Prysm', 'percentage': 0.5735648818137964}, {'client': 'Teku', 'percentage': 0.001929570670525808}], 'networkPenetration': 0.004875032473155525, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.005063291139240506}, {'relayer': 'ultra_sound_money', 'percentage': 0.3468354430379747}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.42278481012658226}, {'relayer': 'no_mev_boost', 'percentage': 0.007594936708860759}, {'relayer': 'flashbots', 'percentage': 0.18227848101265823}, {'relayer': 'agnostic', 'percentage': 0.035443037974683546}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Bloxstaking', 'aprPercentage': 4.88}, {'id': 'StakeWise Labs', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 1549, 'avgCorrectness': 0.9911297886964764, 'avgInclusionDelay': 1.025921921892341, 'avgUptime': 0.9986707245842171, 'avgValidatorEffectiveness': 96.63512114509618, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.49390243902439024}, {'client': 'Nimbus', 'percentage': 0.012195121951219513}, {'client': 'Teku', 'percentage': 0.49390243902439024}], 'networkPenetration': 0.0020958715794942846, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.17901234567901234}, {'relayer': 'agnostic', 'percentage': 0.32098765432098764}, {'relayer': 'blocknative', 'percentage': 0.16666666666666666}, {'relayer': 'ultra_sound_money', 'percentage': 0.3271604938271605}, {'relayer': 'no_mev_boost', 'percentage': 0.006172839506172839}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'StakeWise Labs', 'aprPercentage': 4.76}, {'id': 'XHash', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 1335, 'avgCorrectness': 0.9959948770573308, 'avgInclusionDelay': 1.017659356132019, 'avgUptime': 0.999878063169219, 'avgValidatorEffectiveness': 97.90271166751971, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.001034126163391934}, {'client': 'Prysm', 'percentage': 0.9989658738366081}], 'networkPenetration': 0.0018063192760651196, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.1501416430594901}, {'relayer': 'bloxroute_regulated', 'percentage': 0.21813031161473087}, {'relayer': 'aestus', 'percentage': 0.039660056657223795}, {'relayer': 'edennetwork', 'percentage': 0.028328611898016998}, {'relayer': 'ultra_sound_money', 'percentage': 0.1558073654390935}, {'relayer': 'blocknative', 'percentage': 0.08498583569405099}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.2237960339943343}, {'relayer': 'flashbots', 'percentage': 0.09348441926345609}, {'relayer': 'manifold', 'percentage': 0.0056657223796034}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'XHash', 'aprPercentage': 4.62}, {'id': 'Jump Crypto', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 1000, 'avgCorrectness': 0.9936811827711054, 'avgInclusionDelay': 1.0219393434207382, 'avgUptime': 0.9993498412698412, 'avgValidatorEffectiveness': 97.23858990271765, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.8631415241057543}, {'client': 'Nimbus', 'percentage': 0.0015552099533437014}, {'client': 'Prysm', 'percentage': 0.13530326594090203}], 'networkPenetration': 0.0013530481468652582, 'relayerPercentages': [{'relayer': 'bloxroute_regulated', 'percentage': 0.7571428571428571}, {'relayer': 'flashbots', 'percentage': 0.24285714285714285}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Jump Crypto', 'aprPercentage': 4.6}, {'id': 'Ebunker', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 524, 'avgCorrectness': 0.9934322392503543, 'avgInclusionDelay': 1.0211397632375883, 'avgUptime': 0.999540470947034, 'avgValidatorEffectiveness': 97.30198179435276, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.1962864721485411}, {'client': 'Prysm', 'percentage': 0.8010610079575596}, {'client': 'Teku', 'percentage': 0.002652519893899204}], 'networkPenetration': 0.0007089972289573952, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 0.1323529411764706}, {'relayer': 'ultra_sound_money', 'percentage': 0.35294117647058826}, {'relayer': 'agnostic', 'percentage': 0.4117647058823529}, {'relayer': 'blocknative', 'percentage': 0.10294117647058823}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Ebunker', 'aprPercentage': 5.45}, {'id': 'Finoa', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 250, 'avgCorrectness': 0.9925403531413252, 'avgInclusionDelay': 1.0201738184940643, 'avgUptime': 0.9996926984126984, 'avgValidatorEffectiveness': 97.30700362564548, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.12962962962962962}, {'client': 'Nimbus', 'percentage': 0.024691358024691357}, {'client': 'Teku', 'percentage': 0.845679012345679}], 'networkPenetration': 0.00033826203671631454, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Finoa', 'aprPercentage': 3.53}, {'id': 'snc.xyz', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 221, 'avgCorrectness': 0.9935630609797361, 'avgInclusionDelay': 1.0216443325905327, 'avgUptime': 0.9996315192716692, 'avgValidatorEffectiveness': 97.30257516396266, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.000299023640457222, 'relayerPercentages': [{'relayer': 'ultra_sound_money', 'percentage': 0.9411764705882353}, {'relayer': 'no_mev_boost', 'percentage': 0.058823529411764705}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'snc.xyz', 'aprPercentage': 4.23}, 
      {'id': 'SenseiNode', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 192, 'avgCorrectness': 0.9809404595495259, 'avgInclusionDelay': 1.0506775040756493, 'avgUptime': 0.9959623015873016, 'avgValidatorEffectiveness': 93.19754426398607, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.00025978524419812955, 'relayerPercentages': [{'relayer': 'ultra_sound_money', 'percentage': 0.08695652173913043}, {'relayer': 'blocknative', 'percentage': 0.21739130434782608}, {'relayer': 'bloxroute_regulated', 'percentage': 0.13043478260869565}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.13043478260869565}, {'relayer': 'flashbots', 'percentage': 0.30434782608695654}, {'relayer': 'edennetwork', 'percentage': 0.13043478260869565}], 'nodeOperatorCount': 2, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'SenseiNode', 'aprPercentage': 3.9}, {'id': 'VeriHash', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 191, 'avgCorrectness': 0.9922467964309275, 'avgInclusionDelay': 1.0247556091612413, 'avgUptime': 0.9977029834621457, 'avgValidatorEffectiveness': 96.68154167659868, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.6060606060606061}, {'client': 'Teku', 'percentage': 0.3939393939393939}], 'networkPenetration': 0.00025843219605126426, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 0.1}, {'relayer': 'ultra_sound_money', 'percentage': 0.05}, {'relayer': 'agnostic', 'percentage': 0.05}, {'relayer': 'aestus', 'percentage': 0.05}, {'relayer': 'blocknative', 'percentage': 0.15}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.25}, {'relayer': 'flashbots', 'percentage': 0.35}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'VeriHash', 'aprPercentage': 3.96}, {'id': 'Prysm Client Team', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.9955700184019143, 'avgInclusionDelay': 1.0158429899289203, 'avgUptime': 0.99994708994709, 'avgValidatorEffectiveness': 98.0326744163054, 'clientPercentages': [{'client': 'Prysm', 'percentage': 1.0}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}, {'name': 'client_team', 'path': None, 'idType': None}], 'displayName': 'Prysm Client Team', 'aprPercentage': 3.56}, {'id': 'Lighthouse Client Team', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.9946959974479633, 'avgInclusionDelay': 1.0180421350668365, 'avgUptime': 0.9997663139329805, 'avgValidatorEffectiveness': 97.73502956643297, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}, {'name': 'client_team', 'path': None, 'idType': None}], 'displayName': 'Lighthouse Client Team', 'aprPercentage': 4.01}, {'id': 'Teku Client Team', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.9924418878223226, 'avgInclusionDelay': 1.0207818675889329, 'avgUptime': 0.9995061728395063, 'avgValidatorEffectiveness': 97.23308858857054, 'clientPercentages': [{'client': 'Teku', 'percentage': 1.0}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}, {'name': 'client_team', 'path': None, 'idType': None}], 'displayName': 'Teku Client Team', 'aprPercentage': 3.24}, {'id': 'Nimbus Client Team', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.9929111044436583, 'avgInclusionDelay': 1.0222697900200173, 'avgUptime': 0.9845987654320987, 'avgValidatorEffectiveness': 95.69371655780313, 'clientPercentages': [{'client': 'Nimbus', 'percentage': 1.0}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Nimbus Client Team', 'aprPercentage': 3.38}, {'id': 'T-Systems', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.9906790454138277, 'avgInclusionDelay': 1.0409038787626566, 'avgUptime': 0.9959038800705469, 'avgValidatorEffectiveness': 94.9495423230297, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'aestus', 'percentage': 0.16666666666666666}, {'relayer': 'agnostic', 'percentage': 0.16666666666666666}, {'relayer': 'ultra_sound_money', 'percentage': 0.3333333333333333}, {'relayer': 'bloxroute_maxprofit', 'percentage': 0.3333333333333333}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'T-Systems', 'aprPercentage': 3.49}, {'id': 'Erigon Client Team', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 144, 'avgCorrectness': 0.946656980437704, 'avgInclusionDelay': 1.140015336529191, 'avgUptime': 0.9832319223985889, 'avgValidatorEffectiveness': 82.04258062687084, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.8888888888888888}, {'client': 'Nimbus', 'percentage': 0.013888888888888888}, {'client': 'Prysm', 'percentage': 0.09722222222222222}], 'networkPenetration': 0.00019483893314859715, 'relayerPercentages': [{'relayer': 'no_mev_boost', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Erigon Client Team', 'aprPercentage': 3.28}, {'id': 'Gateway.fm', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 105, 'avgCorrectness': 0.9866219046868783, 'avgInclusionDelay': 1.0368256161337042, 'avgUptime': 0.9978594104308391, 'avgValidatorEffectiveness': 95.08060158443801, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 0.0001420700554208521, 'relayerPercentages': [{'relayer': 'bloxroute_regulated', 'percentage': 0.75}, {'relayer': 'blocknative', 'percentage': 0.25}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Gateway.fm', 'aprPercentage': 3.73}, {'id': 'Northstake', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 69, 'avgCorrectness': 0.9951694386278869, 'avgInclusionDelay': 1.0184213196564798, 'avgUptime': 0.9999263860133425, 'avgValidatorEffectiveness': 97.74554961425568, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 9.336032213370281e-05, 'relayerPercentages': [{'relayer': 'bloxroute_maxprofit', 'percentage': 0.125}, {'relayer': 'ultra_sound_money', 'percentage': 0.125}, {'relayer': 'blocknative', 'percentage': 0.25}, {'relayer': 'flashbots', 'percentage': 0.125}, {'relayer': 'bloxroute_regulated', 'percentage': 0.375}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Northstake', 'aprPercentage': 4.91}, {'id': 'Coinbase Cloud', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 26, 'avgCorrectness': 0.9960031584002865, 'avgInclusionDelay': 1.0152384673618404, 'avgUptime': 0.99997557997558, 'avgValidatorEffectiveness': 98.1332785342785, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 3.517925181849671e-05, 'relayerPercentages': [{'relayer': 'agnostic', 'percentage': 0.5}, {'relayer': 'ultra_sound_money', 'percentage': 0.5}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Coinbase Cloud', 'aprPercentage': 3.68}, {'id': 'PierTwo', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 23, 'avgCorrectness': 0.9930432499835926, 'avgInclusionDelay': 1.0221640930441875, 'avgUptime': 0.9997791580400276, 'avgValidatorEffectiveness': 97.19243749696746, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 1.0}], 'networkPenetration': 2.841401108417042e-05, 'relayerPercentages': [], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'PierTwo', 'aprPercentage': 2.84}, {'id': 'Anyblock Analytics', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 13, 'avgCorrectness': 0.996206015013108, 'avgInclusionDelay': 1.0191490401055152, 'avgUptime': 0.9998046398046397, 'avgValidatorEffectiveness': 97.77196687997578, 'clientPercentages': [{'client': 'Lighthouse', 'percentage': 0.0034904013961605585}, {'client': 'Nimbus', 'percentage': 0.0017452006980802793}, {'client': 'Prysm', 'percentage': 0.9912739965095986}, {'client': 'Teku', 'percentage': 0.0034904013961605585}], 'networkPenetration': 1.7589625909248354e-05, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Anyblock Analytics', 'aprPercentage': 4.71}, {'id': 'Blockshard', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 4, 'avgCorrectness': 0.9959246321583571, 'avgInclusionDelay': 1.0168307399174341, 'avgUptime': 0.9996825396825396, 'avgValidatorEffectiveness': 97.98058899384324, 'clientPercentages': [{'client': 'Nimbus', 'percentage': 1.0}], 'networkPenetration': 5.412192587461032e-06, 'relayerPercentages': [{'relayer': 'flashbots', 'percentage': 1.0}], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Blockshard', 'aprPercentage': 7.92}, {'id': 'Chainnodes', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 3, 'avgCorrectness': 0.9914529914529915, 'avgInclusionDelay': 1.0273363000635727, 'avgUptime': 0.9987301587301587, 'avgValidatorEffectiveness': 96.42456435794274, 'clientPercentages': [{'client': 'Unknown', 'percentage': 1.0}], 'networkPenetration': 4.059144440595774e-06, 'relayerPercentages': [], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Chainnodes', 'aprPercentage': 2.84}, {'id': 'Brick Towers', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 2, 'avgCorrectness': 0.9879250079440737, 'avgInclusionDelay': 1.0241499841118527, 'avgUptime': 0.9990476190476191, 'avgValidatorEffectiveness': 96.38715286960364, 'clientPercentages': [{'client': 'Unknown', 'percentage': 1.0}], 'networkPenetration': 2.706096293730516e-06, 'relayerPercentages': [], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'selfReport', 'path': None, 'idType': None}, {'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Brick Towers', 'aprPercentage': 2.83}, {'id': 'Audit.one', 'idType': 'nodeOperator', 'timeWindow': '7d', 'validatorCount': 1, 'avgCorrectness': 0.9955555555555555, 'avgInclusionDelay': 1.0133333333333334, 'avgUptime': 1.0, 'avgValidatorEffectiveness': 98.27150991554119, 'clientPercentages': [{'client': 'Unknown', 'percentage': 1.0}], 'networkPenetration': 1.353048146865258e-06, 'relayerPercentages': [], 'nodeOperatorCount': 1, 'operatorTags': [{'name': 'operator', 'path': None, 'idType': None}], 'displayName': 'Audit.one', 'aprPercentage': 2.85}], 'next': None}}
    print_data("fetch", response)
    return response
  else:
    url = "https://api.rated.network/v0/eth/operators?window=7d&idType=nodeOperator&size=100"
    payload = {}
    headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': rated_token
    }
    response = fetch(url, "GET", payload, headers)
    return response

def process_rated_operator_node_data(raw_data):
  # # example rated raw data:
  # raw_data = { 'attempts': 1, 'data': { 'data': [ 
  #   { 
  #     'aprPercentage': 4.93,
  #     'avgCorrectness': 0.9949509406954944,
  #     'avgInclusionDelay': 1.017948702586212,
  #     'avgUptime': 0.9998280828900458,
  #     'avgValidatorEffectiveness': 97.76418156450255,
  #     'clientPercentages': [  { 'client': 'Lighthouse',
  #                               'percentage': 0.333947045414694},
  #                             { 'client': 'Nimbus',
  #                               'percentage': 0.0005260389268805891},
  #                             { 'client': 'Prysm',
  #                               'percentage': 0.6386989303875154},
  #                             { 'client': 'Teku',
  #                               'percentage': 0.026827985270910047}],
  #     'displayName': 'Kiln',
  #     'id': 'Kiln',
  #     'idType': 'nodeOperator',
  #     'networkPenetration': 0.032216076376861795,
  #     'nodeOperatorCount': 4,
  #     'operatorTags': [ { 'idType': None,
  #                         'name': 'selfReport',
  #                         'path': None},
  #                       { 'idType': None,
  #                         'name': 'operator',
  #                         'path': None}],
  #     'relayerPercentages': [ { 'percentage': 0.09717868338557993,
  #                               'relayer': 'blocknative'},
  #                             { 'percentage': 0.012763098969995522,
  #                               'relayer': 'edennetwork'},
  #                             { 'percentage': 0.0006717420510523958,
  #                               'relayer': 'no_mev_boost'},
  #                             { 'percentage': 0.025526197939991044,
  #                               'relayer': 'aestus'},
  #                             { 'percentage': 0.17129422301836095,
  #                               'relayer': 'ultra_sound_money'},
  #                             { 'percentage': 0.24406627854903717,
  #                               'relayer': 'bloxroute_maxprofit'},
  #                             { 'percentage': 0.001567398119122257,
  #                               'relayer': 'manifold'},
  #                             { 'percentage': 0.23510971786833856,
  #                               'relayer': 'bloxroute_regulated'},
  #                             { 'percentage': 0.1334527541424093,
  #                               'relayer': 'agnostic'},
  #                             { 'percentage': 0.07836990595611286,
  #                               'relayer': 'flashbots'}],
  #     'timeWindow': '7d',
  #     'validatorCount': 23810
  #   }]}}
  return


def get_edi_marketshare_data():
  if use_test_data:
    # response split into multiple lines so it can be collapsed
    response = {'status': 200, 'attempts': 1, 'data': [
      {'name': 'Attestant', 'website': 'https://www.attestant.io/', 'sourceLink': 'https://www.attestant.io/posts/helping-client-diversity/', 'twitter': 'https://twitter.com/attestantio', 'reliable': False, 'clients': [{'name': 'NoGeth', 'tooltip': 'Geth is not used for attestations (no supermajority client risk). See the link for details.', 'percent': 100}], 'ratedId': 'Attestant', 'type': 'operator'}, {'name': 'Ethpool', 'website': 'https://ethpool.org/', 'source': 'Support (Discord)', 'twitter': 'https://twitter.com/ethpool_staking', 'reliable': True, 'clients': [{'name': 'Nethermind', 'percent': 100}], 'ratedId': None, 'type': 'pool'},{'name': 'StakeWise', 'website': 'https://stakewise.io/', 'source': 'Support (Discord), approximate numbers', 'twitter': 'https://twitter.com/stakewise_io', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 42.12}, {'name': 'Nethermind', 'percent': 28.94}, {'name': 'Besu', 'percent': 28.94}], 'ratedId': 'StakeWise', 'type': 'pool'}, {'name': 'Rocket Pool', 'website': 'https://rocketpool.net/', 'source': 'Discord (Tool developed by 0xinvis.eth)', 'twitter': 'https://twitter.com/Rocket_Pool', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 46.56}, {'name': 'Nethermind', 'percent': 19.3}, {'name': 'Besu', 'percent': 8.12}, {'name': 'Unknown', 'percent': 26.02}], 'ratedId': 'Rocketpool', 'type': 'pool'}, {'name': 'Lido', 'website': 'https://lido.fi/ethereum', 'sourceLink': 'https://research.lido.fi/t/lido-node-operator-validator-metrics/1431', 'twitter': 'https://twitter.com/LidoFinance', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 84.5}, {'name': 'Nethermind', 'percent': 8.1}, {'name': 'Besu', 'percent': 5.0}, {'name': 'Erigon', 'percent': 2.4}], 'ratedId': 'Lido', 'type': 'pool'}, {'name': 'Staked', 'website': 'https://staking.staked.us/ethereum-staking-options', 'source': 'Support (Discord)', 'twitter': 'https://twitter.com/staked_us', 'reliable': True, 'clients': [{'name': 'Unknown', 'tooltip': 'Allocation unknown, diversified (Geth and Erigon)', 'percent': 100}], 'ratedId': 'Staked.us', 'type': 'operator'}, {'name': 'Allnodes', 'website': 'https://www.allnodes.com/eth2/staking', 'source': 'Support (Discord)', 'twitter': 'https://twitter.com/Allnodes', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 100}], 'ratedId': 'Allnodes', 'type': 'operator'}, {'name': 'Ankr', 'website': 'https://www.ankr.com/staking-crypto/', 'source': 'Data pending', 'twitter': 'https://twitter.com/ankr', 'reliable': False, 'clients': [{'name': 'Geth', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Ankr', 'type': 'pool'}, {'name': 'Blox Staking', 'website': 'https://www.bloxstaking.com/', 'source': 'Support (Discord)', 'twitter': 'https://twitter.com/ssv_network', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 100}], 'ratedId': 'Bloxstaking', 'type': 'pool'}, {'name': 'Binance', 'website': 'https://www.binance.com/en/eth2', 'source': 'Data pending', 'twitter': 'https://twitter.com/binance', 'reliable': False, 'clients': [{'name': 'Geth', 'website': '', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Binance', 'type': 'pool'}, {'name': 'Bitcoin Suisse', 'website': 'https://www.bitcoinsuisse.com/staking/ethereum-2', 'source': 'Data pending', 'twitter': 'https://twitter.com/bitcoinsuisseag', 'reliable': False, 'clients': [{'name': 'Geth', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Bitcoin Suisse', 'type': 'pool'}, {'name': 'Bitfinex', 'website': 'https://staking.bitfinex.com/', 'source': 'Support ("Unfortunately, we are unable to provide you with the specific information you are requesting.")', 'twitter': 'https://twitter.com/bitfinex', 'reliable': False, 'clients': [{'name': 'Geth', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Bitfinex', 'type': 'pool'}, {'name': 'Coinbase', 'website': 'https://www.coinbase.com/earn/staking/ethereum', 'source': 'Data pending', 'twitter': 'https://twitter.com/coinbase', 'reliable': False, 'clients': [{'name': 'Geth', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Coinbase', 'type': 'pool'}, {'name': 'Kraken', 'website': 'https://www.kraken.com/features/staking-coins', 'source': 'Data pending', 'twitter': 'https://twitter.com/krakenfx', 'reliable': False, 'clients': [{'name': 'Geth', 'tooltip': 'Maybe 100% Geth', 'percent': 100}], 'ratedId': 'Kraken', 'type': 'pool'}, {'name': 'P2P.org', 'website': 'https://p2p.org/networks/ethereum', 'source': 'Support (Chat)', 'twitter': 'https://twitter.com/p2pvalidator', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 100}], 'ratedId': 'P2P.ORG - P2P Validator', 'type': 'operator'}, {'name': 'stakefish', 'website': 'https://stake.fish/networks/ethereum', 'source': 'Support (Telegram)', 'twitter': 'https://twitter.com/stakefish', 'reliable': True, 'clients': [{'name': 'Geth', 'percent': 100}], 'ratedId': 'Stakefish', 'type': 'pool'}]}
    print_data("fetch", response)
    return response
  else:
    url = "https://raw.githubusercontent.com/one-three-three-seven/execution-diversity/main/services.json"
    response = fetch(url)
    return response

def process_edi_marketshare_data(raw_data, pool_validator_counts, total_validator_count):
  client_counts = {
    "geth": 0,
    "erigon": 0,
    "nethermind": 0,
    "besu": 0,
    "reth": 0,
    "unknown": 0,
    "other": 0
  }
  nogeth_clients = ["erigon", "nethermind", "besu"]
  validators_represented = 0
  validators_percentage = 0
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  sample_size = 0
  cleaned_data = []
  added_data = []
  removed_data = []
  reformatted_data = []
  calculated_data = []
  marketshare_data = []
  extra_data = {}
  final_data = {}

  # cleaned data
  cleaned_data = copy.deepcopy(raw_data["data"])
  for item in cleaned_data:
    # delete irrelevent keys
    delete_keys = ["source", "sourceLink", "twitter", "website"]
    for key in delete_keys:
      if key in item:
        del item[key]
    for client in item["clients"]:
        # make client names lowercase
        client["name"] = client["name"].lower().strip()
        if "tooltip" in client:
          del client["tooltip"]
        if "website" in client:
          del client["website"]
        # turn client percentages into a decimal
        client["percent"] = client["percent"] / 100
  # pprint(["cleaned_data", cleaned_data])

  # add data
  added_data = copy.deepcopy(cleaned_data)
  for item in added_data:
    if item["ratedId"] in pool_validator_counts:
      validator_count = pool_validator_counts[item["ratedId"]]
      item["validator_count"] = validator_count
  # pprint(["added_data", added_data])

  # remove data with incomplete data
  for item in added_data:
    if item["ratedId"] != None and item["ratedId"] in pool_validator_counts:
      removed_data.append(item)
  # pprint(["removed_data", removed_data])

  # calculate the marketshare for each client
  calculated_data = copy.deepcopy(removed_data)
  for item in calculated_data:
    for client in item["clients"]:
      validator_split = item["validator_count"] * client["percent"]
      # split the number of nogeth validators among nogeth_clients
      if client["name"] == "nogeth":
        for nogeth_client in nogeth_clients:
          client_counts["nogeth_client"] += validator_split
      # tally the number of each explicit client
      else:
        if client["name"] in client_counts:
          client_counts[client["name"]] += validator_split
        # if the client isn't in the clients list, add it to "other"
        else:
          client_counts["other"] += validator_split
    validators_represented += item["validator_count"]
  # pprint(["calculated_data", calculated_data])
  # pprint(["validators_represented", validators_represented])

  # reformat data into a list of dicts
  for key, value in client_counts.items():
    percentage = value / validators_represented
    marketshare_data.append({"name": key, "value": percentage, "accuracy": "no data"})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "edi"
  extra_data["has_majority"] = False
  extra_data["has_supermajority"] = False
  extra_data["danger_client"] = ""
  if sorted_data[0]["value"] >= .50:
    extra_data["has_majority"] = True
    extra_data["danger_client"] = sorted_data[0]["name"]
  if sorted_data[0]["value"] >= .66:
    extra_data["has_supermajority"] = True
  extra_data["top_client"] = sorted_data[0]["name"]
  extra_data["validators_represented"] = validators_represented
  extra_data["validators_total"] = total_validator_count
  validators_percentage = validators_represented / total_validator_count
  extra_data["validators_percentage"] = validators_percentage
  # pprint(["extra_data", extra_data])

  # create final data dict
  final_data["distribution"] = sorted_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_edi")

  return final_data


def edi_marketshare():
  raw_overview_data = get_rated_overview_data()
  save_to_file("../_data/raw/rated_overview_raw.json", raw_overview_data)
  total_validator_count = process_rated_overview_data(raw_overview_data)


  raw_pool_data = get_rated_operator_pool_data()
  save_to_file("../_data/raw/rated_operator_pool_raw.json", raw_pool_data)
  pool_validator_counts = process_rated_operator_pool_data(raw_pool_data)


  # raw_node_data = get_rated_operator_node_data()
  # save_to_file("../_data/raw/rated_operator_node_raw.json", raw_node_data)
  # processed_node_data = process_rated_operator_node_data(raw_node_data)


  raw_marketshare_data = get_edi_marketshare_data()
  save_to_file("../_data/raw/edi_raw.json", raw_marketshare_data)
  processed_marketshare_data = process_edi_marketshare_data(raw_marketshare_data, pool_validator_counts, total_validator_count)

  save_to_file("../_data/edi.json", processed_marketshare_data)


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

  # adjust data where 80% of unaccounted for validators are assumed geth, and the rest is split
  remaining_validators = total_validators - sample_size
  remaining_geth_validators = round(remaining_validators * 0.8)
  unknown_validators = next((item for item in filtered_data if item['name'] == "unknown"), None)["value"]
  geth_adjusted = remaining_geth_validators + unknown_validators
  spit_size = 0
  for item in filtered_data:
    if item["name"] != "geth" and item["name"] != "unknown" and item["name"] != "other":
      spit_size += 1
  for item in filtered_data:
    if item["name"] == "geth":
      geth_adjusted += item["value"]
      adjusted_data.append({"name": item["name"], "value": geth_adjusted})
    elif item["name"] == "other":
      adjusted_data.append({"name": item["name"], "value": item["value"]})
    elif item["name"] != "unknown":
      adjusted_value = round(remaining_validators * 0.2 / spit_size) + item["value"]
      adjusted_data.append({"name": item["name"], "value": adjusted_value})
  # pprint(["remaining_validators", remaining_validators])
  # pprint(["remaining_geth_validators", remaining_geth_validators])
  # pprint(["unknown_validators", unknown_validators])
  # pprint(["geth_adjusted", geth_adjusted])
  # pprint(["spit_size", spit_size])
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


def get_blockprint_marketshare_data():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': {'Uncertain': 0, 'Grandine': 0, 'Lighthouse': 33411, 'Lodestar': 1145, 'Nimbus': 4862, 'Other': 0, 'Prysm': 45450, 'Teku': 15458}}
    print_data("fetch", response)
    return response
  else:
    initial_timestamp = 1606824023 # seconds
    initial_epoch = 0
    delta_timestamp = current_time - initial_timestamp # seconds
    current_epoch = math.floor(delta_timestamp / 384)

    # the Blockprint API caches results so fetching data based on an "epoch day" so 
    # everyone that loads the page on an "epoch day" will use the cached results and 
    # their backend doesn't get overloaded
    # Michael Sproul recommends using a 2-week period
    end_epoch = math.floor(current_epoch / 225) * 225
    start_epoch = end_epoch - 3150
    url = f"https://api.blockprint.sigp.io/blocks_per_client/{start_epoch}/{end_epoch}"
    response = fetch(url)
    return response

def get_blockprint_accuracy_data():
  # accuracy of fingerprinting for each client
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': {'clients': {'Lighthouse': {'true_positives': 3644, 'true_negatives': 6921, 'false_positives': 377, 'false_negatives': 37, 'false_negatives_detail': {'Nimbus': 20, 'Prysm': 17}}, 'Nimbus': {'true_positives': 0, 'true_negatives': 10822, 'false_positives': 157, 'false_negatives': 0, 'false_negatives_detail': {}}, 'Prysm': {'true_positives': 5147, 'true_negatives': 5387, 'false_positives': 36, 'false_negatives': 409, 'false_negatives_detail': {'Lighthouse': 376, 'Nimbus': 30, 'Teku': 3}}, 'Teku': {'true_positives': 1615, 'true_negatives': 9234, 'false_positives': 3, 'false_negatives': 127, 'false_negatives_detail': {'Lighthouse': 1, 'Nimbus': 107, 'Prysm': 19}}}, 'nodes': [{'name': 'prysm-subscribe-all', 'label': 'Prysm', 'true_positives': 3648, 'false_negatives': {'Lighthouse': 3, 'Nimbus': 28, 'Teku': 2}, 'latest_slot': 7102453}, {'name': 'prysm-subscribe-none', 'label': 'Prysm', 'true_positives': 1499, 'false_negatives': {'Lighthouse': 373, 'Nimbus': 2, 'Teku': 1}, 'latest_slot': 7102453}, {'name': 'teku-subscribe-all', 'label': 'Teku', 'true_positives': 1615, 'false_negatives': {'Lighthouse': 1, 'Nimbus': 107, 'Prysm': 19}, 'latest_slot': 7102453}, {'name': 'lighthouse-subscribe-none', 'label': 'Lighthouse', 'true_positives': 3644, 'false_negatives': {'Nimbus': 20, 'Prysm': 17}, 'latest_slot': 7102453}]}}
    print_data("fetch", response)
    return response
  else:
    url = "https://api.blockprint.sigp.io/confusion"
    response = fetch(url)
    return response


def process_blockprint_accuracy_data(raw_data):
  # example blockprint raw data:
  # raw_data = {'status': 200, 'attempts': 1, 'data': {
  #   'clients': {
  #     'Lighthouse': {
  #       'true_positives': 3644, 'true_negatives': 6921, 'false_positives': 377, 
  #       'false_negatives': 37, 'false_negatives_detail': {'Nimbus': 20, 'Prysm': 17}}, 
  #     'Nimbus': {
  #       'true_positives': 0, 'true_negatives': 10822, 'false_positives': 157, 
  #       'false_negatives': 0, 'false_negatives_detail': {}}, 
  #     'Prysm': {
  #       'true_positives': 5147, 'true_negatives': 5387, 'false_positives': 36, 
  #       'false_negatives': 409, 'false_negatives_detail': {'Lighthouse': 376, 'Nimbus': 30, 'Teku': 3}}, 
  #     'Teku': {
  #       'true_positives': 1615, 'true_negatives': 9234, 'false_positives': 3, 
  #       'false_negatives': 127, 'false_negatives_detail': {'Lighthouse': 1, 'Nimbus': 107, 'Prysm': 19}}
  #     }, 
  #     'nodes': [
  #       {'name': 'prysm-subscribe-all', 'label': 'Prysm', 'true_positives': 3648, 
  #         'false_negatives': {'Lighthouse': 3, 'Nimbus': 28, 'Teku': 2}, 'latest_slot': 7102453}, 
  #       {'name': 'prysm-subscribe-none', 'label': 'Prysm', 'true_positives': 1499, 
  #         'false_negatives': {'Lighthouse': 373, 'Nimbus': 2, 'Teku': 1}, 'latest_slot': 7102453}, 
  #       {'name': 'teku-subscribe-all', 'label': 'Teku', 'true_positives': 1615, 
  #         'false_negatives': {'Lighthouse': 1, 'Nimbus': 107, 'Prysm': 19}, 'latest_slot': 7102453}, 
  #       {'name': 'lighthouse-subscribe-none', 'label': 'Lighthouse', 'true_positives': 3644, 
  #         'false_negatives': {'Nimbus': 20, 'Prysm': 17}, 'latest_slot': 7102453}
  #     ]}}

  # calculate the accuracy for each client
  accuracy_data = []
  for key, value in raw_data["data"]["clients"].items():
    if (value["true_positives"] == 0 and value["false_negatives"] == 0):
      accuracy = "no data";
    elif (value["true_positives"] == 0 and value["false_negatives"] != 0):
      accuracy = "0";
    else:
      accuracy = round(value["true_positives"] / (value["true_positives"] + value["false_negatives"]), 6)
    accuracy_data.append({"name": key.lower(), "value": accuracy})
  print_data("processed", accuracy_data, "blockprint_accuracy_data")
  return accuracy_data

def process_blockprint_marketshare_data(raw_marketshare_data, processed_accuracy_data):
  # example blockprint raw data:
  # raw_marketshare_data = {'status': 200, 'attempts': 1, 'data': {
  #   'Uncertain': 0, 
  #   'Grandine': 0, 
  #   'Lighthouse': 33411, 
  #   'Lodestar': 1145, 
  #   'Nimbus': 4862, 
  #   'Other': 0, 
  #   'Prysm': 45450, 
  #   'Teku': 15458
  #   }}

  main_clients = ["lighthouse", "nimbus", "teku", "prysm", "lodestar", "erigon", "grandine"]
  threshold_percentage = 0.5 # represented as a percent, not a decimal
  sample_size = 0
  reformatted_data = []
  filtered_data = [{"name": "other", "value": 0}]
  marketshare_data = []
  extra_data = {}
  final_data = {}

  # reformat data into a list of dicts
  for key, value in raw_marketshare_data["data"].items():
    reformatted_data.append({"name": key.lower(), "value": value})
    sample_size += value
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
    accuracy = "no data"
    for x in processed_accuracy_data:
      if x["name"] == item["name"]:
        accuracy = x["value"]
    marketshare_data.append({"name": item["name"], "value": marketshare, "accuracy": accuracy})
  # pprint(["marketshare_data", marketshare_data])

  # sort the list by marketshare descending
  sorted_data = sorted(marketshare_data, key=lambda k : k['value'], reverse=True)
  # pprint(["sorted_data", sorted_data])

  # supplemental data
  extra_data["data_source"] = "blockprint"
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
  # final_data["accuracy"] = processed_accuracy_data
  final_data["other"] = extra_data
  print_data("processed", final_data, "final_data_blockprint")

  return final_data


def blockprint_marketshare():
  raw_marketshare_data = get_blockprint_marketshare_data()
  save_to_file("../_data/raw/blockprint_raw.json", raw_marketshare_data)
  raw_accuracy_data = get_blockprint_accuracy_data()
  save_to_file("../_data/raw/blockprint_accuracy_raw.json", raw_accuracy_data)
  processed_accuracy_data = process_blockprint_accuracy_data(raw_accuracy_data)
  processed_marketshare_data = process_blockprint_marketshare_data(raw_marketshare_data, processed_accuracy_data)
  save_to_file("../_data/blockprint.json", processed_marketshare_data)


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


def get_migalabs_marketshare_data():
  if use_test_data:
    response = {'status': 200, 'attempts': 1, 'data': [{"timestamp":"2023-10-03T04:37:09Z","data":[{"client_name":"lighthouse","node_count":2867},{"client_name":"prysm","node_count":2206},{"client_name":"teku","node_count":1303},{"client_name":"nimbus","node_count":836},{"client_name":"lodestar","node_count":252},{"client_name":"grandine","node_count":213},{"client_name":"unknown","node_count":28}]}]}
    print_data("fetch", response)
    return response
  else:
    url = "https://monitoreth.io/data-api/api/eth/v1/nodes/consensus/validators/client_diversity"
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
  # if day == "Saturday" or current_time < 1706217143:
  #   edi_marketshare()
  #   rated_marketshare()
  supermajority_marketshare()
  blockprint_marketshare()
  ethernodes_marketshare()
  migalabs_marketshare()


get_data()



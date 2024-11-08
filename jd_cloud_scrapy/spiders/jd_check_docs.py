# pip uninstall pyOpenSSL
# pip install pyOpenSSL

from pathlib import Path
import scrapy
import re
import time
import os
from enum import Enum
from pydantic import BaseModel
from markdownify import markdownify as md

incorrect_filename="/tmp/incorrect_docs.csv"

class json_doc(BaseModel):
    content: str
    title: str
    product: str
    url: str


class Reason(Enum):
    StartWithUnicode = 'start_with_unicode'
    IsHtml = 'is_html'


class bad_doc_json(BaseModel):
    url: str
    incorrect_reason: Reason

    def __str__(self):
        return str(self.value)


class QuotesSpider(scrapy.Spider):
    name = "jd_check_docs"
    root_dir = "/tmp/"   

    def start_requests(self):
        urls = [
            "https://docs.jdcloud.com/cn/virtual-machines/learning",
            "https://docs.jdcloud.com/cn/iavm/learning",
            "https://docs.jdcloud.com/cn/availability-group/product-overview",
            "https://docs.jdcloud.com/cn/dedicated-host/product-overview",
            "https://docs.jdcloud.com/cn/jd-workspaces/learning",
            "https://docs.jdcloud.com/cn/cloud-physical-server/product-overview",
            "https://docs.jdcloud.com/cn/Function-Compute/product-overview",
            "https://docs.jdcloud.com/cn/native-container/product-overview",
            "https://docs.jdcloud.com/cn/container-registry/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-kubernetes/product-overview",
            "https://docs.jdcloud.com/cn/gcs/overview",
            "https://docs.jdcloud.com/cn/edge-physical-computing-service/product-overview",
            "https://docs.jdcloud.com/cn/object-storage-service/learning",
            "https://docs.jdcloud.com/cn/cloud-disk-service/learning",
            "https://docs.jdcloud.com/cn/storage-gateway/product-overview",
            "https://docs.jdcloud.com/cn/cloud-file-service/learning",
            "https://docs.jdcloud.com/cn/rds/learning",
            "https://docs.jdcloud.com/cn/tidb-service/product-overview",
            "https://docs.jdcloud.com/cn/drds/product-overview",
            "https://docs.jdcloud.com/cn/starlitedb/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-mongodb/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-redis/learning",
            "https://docs.jdcloud.com/cn/jcs-for-memcached/product-overview",
            "https://docs.jdcloud.com/cn/graph/product-introduce",
            "https://docs.jdcloud.com/cn/column-oriented-storage/product-overview",
            "https://docs.jdcloud.com/cn/jchdb/product-overview",
            "https://docs.jdcloud.com/cn/starwift/product-overview",
            "https://docs.jdcloud.com/cn/data-transmission-service/product-overview",
            "https://docs.jdcloud.com/cn/smartdba/product-overview",
            "https://docs.jdcloud.com/cn/dbs/product-overview",
            "https://docs.jdcloud.com/cn/dms/product-overview",
            "https://docs.jdcloud.com/cn/virtual-private-cloud/learning",
            "https://docs.jdcloud.com/cn/network-load-balancer/learning",
            "https://docs.jdcloud.com/cn/elastic-network-interface/product-overview",
            "https://docs.jdcloud.com/cn/nat-gateway/product-overview",
            "https://docs.jdcloud.com/cn/elastic-ip/release-records",
            "https://docs.jdcloud.com/cn/shared-bandwidth-package/release-records",
            "https://docs.jdcloud.com/cn/sd-wan/product-overview",
            "https://docs.jdcloud.com/cn/application-load-balancer/learning",
            "https://docs.jdcloud.com/cn/distributed-network-load-balancer/learning",
            "https://docs.jdcloud.com/cn/direct-connection/product-overview",
            "https://docs.jdcloud.com/cn/vpn/release-records",
            "https://docs.jdcloud.com/cn/mcdn/product-overview",
            "https://docs.jdcloud.com/cn/cdn/product-overview",
            "https://docs.jdcloud.com/cn/jez/product-overview",
            "https://docs.jdcloud.com/cn/message-queue/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-kafka/productfeatureupdate",
            "https://docs.jdcloud.com/cn/api-gateway/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-elasticsearch/product-news",
            "https://docs.jdcloud.com/cn/jd-distributed-service-framework/product-overview",
            "https://docs.jdcloud.com/cn/notification-service/product-overview",
            "https://docs.jdcloud.com/cn/jcs-for-zookeeper/product-overview",
            "https://docs.jdcloud.com/cn/jimkv/product-feature-update",
            "https://docs.jdcloud.com/cn/RocketMQ/product-feature-update",
            "https://docs.jdcloud.com/cn/mesh/product-overview",
            "https://docs.jdcloud.com/cn/jdfusion/product-overview",
            "https://docs.jdcloud.com/cn/cloud-cabinet-service/product-overview",
            "https://docs.jdcloud.com/cn/edge-cloud-cabinet-service/product-overview",
            "https://docs.jdcloud.com/cn/haas-server/product-overview",
            "https://docs.jdcloud.com/cn/direct-link/product-overview",
            "https://docs.jdcloud.com/cn/cabinet-physical-computing/product-overview",
            "https://docs.jdcloud.com/cn/modular-data-center-mdc/product-overview",
            "https://docs.jdcloud.com/cn/co-location/product-overview",
            "https://docs.jdcloud.com/cn/monoline-and-bgp-bandwidth/product-overview",
            "https://docs.jdcloud.com/cn/distributed-access-service/product-overview",
            "https://docs.jdcloud.com/cn/customized-inspection/product-overview",
            "https://docs.jdcloud.com/cn/it-equipment-installation/product-overview",
            "https://docs.jdcloud.com/cn/idc-local-technical-support/product-overview",
            "https://docs.jdcloud.com/cn/network-architecture-design-service/product-overview",
            "https://docs.jdcloud.com/cn/idc-assets-management/product-overview",
            "https://docs.jdcloud.com/cn/server-and-network-monitor-service/product-overview",
            "https://docs.jdcloud.com/cn/one-stop-hardware-solution-service/product-overview",
            "https://docs.jdcloud.com/cn/jd-cloud-drs/product-overview",
            "https://docs.jdcloud.com/cn/jdmigration/product-overview",
            "https://docs.jdcloud.com/cn/private-bare-metal-service/product-overview",
            "https://docs.jdcloud.com/cn/endpoint-security/product-overview",
            "https://docs.jdcloud.com/cn/starshield/announcement",
            "https://docs.jdcloud.com/cn/anti-ddos-basic/product-overview",
            "https://docs.jdcloud.com/cn/anti-ddos-protection-package/product-overview",
            "https://docs.jdcloud.com/cn/anti-ddos-pro/learning",
            "https://docs.jdcloud.com/cn/anti-ddos-premium-service/product-overview",
            "https://docs.jdcloud.com/cn/cloudfw/01-versiondefine",
            "https://docs.jdcloud.com/cn/situation-awareness/product-overview",
            "https://docs.jdcloud.com/cn/security-operation-center/01-versiondefine",
            "https://docs.jdcloud.com/cn/bastion/product-overview",
            "https://docs.jdcloud.com/cn/jdcloudhsm/product-overview",
            "https://docs.jdcloud.com/cn/ssl-certificate/learning",
            "https://docs.jdcloud.com/cn/key-management-service/product-overview",
            "https://docs.jdcloud.com/cn/database-audit/product-overview",
            "https://docs.jdcloud.com/cn/web-application-firewall/what-is-webapplication-firewall",
            "https://docs.jdcloud.com/cn/application-security-gateway/",
            "https://docs.jdcloud.com/cn/nf1-adc/what-is-nf1",
            "https://docs.jdcloud.com/cn/appdefend/product-overview",
            "https://docs.jdcloud.com/cn/apphunter/product-overview",
            "https://docs.jdcloud.com/cn/website-threat-inspector/product-overview",
            "https://docs.jdcloud.com/cn/risk-detection/product-overview",
            "https://docs.jdcloud.com/cn/content-moderation/what-is-content-moderation",
            "https://docs.jdcloud.com/cn/device-fingerprint/product-overview",
            "https://docs.jdcloud.com/cn/captcha/product-overview",
            "https://docs.jdcloud.com/cn/electronic-signature/product-overview",
            "https://docs.jdcloud.com/cn/real-name-authentication/product-overview",
            "https://docs.jdcloud.com/cn/secsolution/overview",
            "https://docs.jdcloud.com/cn/unified-secure-managed-service-platform/product-overview",
            "https://docs.jdcloud.com/cn/baseline-check-service/product-overview",
            "https://docs.jdcloud.com/cn/vulnerability-scan-service/product-overview",
            "https://docs.jdcloud.com/cn/penetration-test-service/product-overview",
            "https://docs.jdcloud.com/cn/incident-response-service/product-overview",
            "https://docs.jdcloud.com/cn/cybersecurity-classified-protection-consulting-service/product-overview",
            "https://docs.jdcloud.com/cn/important-cybersecurity-guarantees-service/product-overview",
            "https://docs.jdcloud.com/cn/important-cybersecurity-guarantees-service/product-overview",
            "https://docs.jdcloud.com/cn/information-security-training/product-overview",
            "https://docs.jdcloud.com/cn/security-notification-service/product-overview",
            "https://docs.jdcloud.com/cn/security-consulting-service/product-overview",
            "https://docs.jdcloud.com/cn/code-audit-service/product-overview",
            "https://docs.jdcloud.com/cn/pci-dss-compliance-service/product-overview",
            "https://docs.jdcloud.com/cn/security-crowdsourced-testing-service/product-overview",
            "https://docs.jdcloud.com/cn/security-attack-and-defense-drill-service/product-overview",
            "https://docs.jdcloud.com/cn/jd-cloud-dns/learning",
            "https://docs.jdcloud.com/cn/private-zone/announce",
            "https://docs.jdcloud.com/cn/ai-community/",
            "https://docs.jdcloud.com/cn/yanxi-cap/product-overview",
            "https://docs.jdcloud.com/cn/modelservice/product-overview",
            "https://docs.jdcloud.com/cn/monitoring/learning",
            "https://docs.jdcloud.com/cn/log-service/product-overview",
            "https://docs.jdcloud.com/cn/cloudevents/product-overview",
            "https://docs.jdcloud.com/cn/sgm/product-overview",
            "https://docs.jdcloud.com/cn/sgm-web/Product-Overview",
            "https://docs.jdcloud.com/cn/sgm-mobile/Product-Overview",
            "https://docs.jdcloud.com/cn/codecommit/product-overview",
            "https://docs.jdcloud.com/cn/perftest/product-overview",
            "https://docs.jdcloud.com/cn/artifacts/product-overview",
            "https://docs.jdcloud.com/cn/bizdevops/product-overview",
            "https://docs.jdcloud.com/cn/joybuilder/product-overview",
            "https://docs.jdcloud.com/cn/sbom/product-overview",
            "https://docs.jdcloud.com/cn/joycoder/product-overview",
            "https://docs.jdcloud.com/cn/dbizdevopstraining/overview",
            "https://docs.jdcloud.com/cn/iam/product-overview",
            "https://docs.jdcloud.com/cn/devops/product-overview",
            "https://docs.jdcloud.com/cn/audit-trail/product-overview",
            "https://docs.jdcloud.com/cn/tag-service/product-overview",
            "https://docs.jdcloud.com/cn/ias/overview",
            "https://docs.jdcloud.com/cn/devagile/product-overview",
            "https://docs.jdcloud.com/cn/organization-management/Introduction/Product-Overview",
            "https://docs.jdcloud.com/cn/peie/product-overview",
            "https://docs.jdcloud.com/cn/apm/product-overview",
            "https://docs.jdcloud.com/cn/fireeye/product-overview",
            "https://docs.jdcloud.com/cn/mobile-gateway/product-overview",
            "https://docs.jdcloud.com/cn/umap/product-overview",
            "https://docs.jdcloud.com/cn/h5-scan/product-overview",
            "https://docs.jdcloud.com/cn/advisor/product-overview",
            "https://docs.jdcloud.com/cn/amc/product-overview",
            "https://docs.jdcloud.com/cn/domain-name-service/learning",
            "https://docs.jdcloud.com/cn/jdcloud-site/learning",
            "https://docs.jdcloud.com/cn/icp-license-service/introduction",
            "https://docs.jdcloud.com/cn/yuntuike/settle-in",
            "https://docs.jdcloud.com/cn/text-message/product-overview",
            "https://docs.jdcloud.com/cn/rich-media-sms/product-overview",
            "https://docs.jdcloud.com/cn/live-video/product-overview",
            "https://docs.jdcloud.com/cn/media-processing-service/product-overview",
            "https://docs.jdcloud.com/cn/video-on-demand/product-overview",
            "https://docs.jdcloud.com/cn/video-quality-detection/product-overview",
            "https://docs.jdcloud.com/cn/mobile-live-video-sdk/product-overview",
            "https://docs.jdcloud.com/cn/short-video-service-sdk/product-overview",
            "https://docs.jdcloud.com/cn/player-service-sdk/product-overview",
            "https://docs.jdcloud.com/cn/real-time-communication/product-overview",
            "https://docs.jdcloud.com/cn/jdt-meeting/product-overview",
            "https://docs.jdcloud.com/cn/enterprise-live/product-overview",
            "https://docs.jdcloud.com/cn/vr-live/product-overview",
            "https://docs.jdcloud.com/cn/vr-video-on-demand/product-overview",
            "https://docs.jdcloud.com/cn/vr-player-service-sdk/product-overview",
            "https://docs.jdcloud.com/cn/huizhanyunsaas/product-overview",
            "https://docs.jdcloud.com/cn/jdcloudmail/product-overview",
            "https://docs.jdcloud.com/cn/jd-blockchain-open-platform/product-overview",
            "https://docs.jdcloud.com/cn/finance-taxation/product-overview",
            "https://docs.jdcloud.com/cn/data-factory/product-overview",
            "https://docs.jdcloud.com/cn/data-integration/product-overview",
            "https://docs.jdcloud.com/cn/data-compute/product-overview",
            "https://docs.jdcloud.com/cn/stream-hub/product-overview",
            "https://docs.jdcloud.com/cn/stream-compute/product-overview",
            "https://docs.jdcloud.com/cn/bi-report/product-overview",
            "https://docs.jdcloud.com/cn/jd-mapreduce/version-overview",
            "https://docs.jdcloud.com/cn/data-visualization/product-overview",
            "https://docs.jdcloud.com/cn/iot-data-analysis-service/product-overview",
            "https://docs.jdcloud.com/cn/iot-aep/product-overview",
            "https://docs.jdcloud.com/cn/device-access/product-overview",
            "https://docs.jdcloud.com/cn/device-access/product-overview",
            "https://docs.jdcloud.com/cn/iot-jitdb/product-overview",
            "https://docs.jdcloud.com/cn/iot-link-service/product-overview",
            "https://docs.jdcloud.com/cn/rt-thread-for-jd/product-overview",
            "https://docs.jdcloud.com/cn/iot-devfss/product-overview",
            "https://docs.jdcloud.com/cn/iot-device-identity/product-overview",
            "https://docs.jdcloud.com/cn/aiot-cv/product-overview",
            "https://docs.jdcloud.com/cn/iot-carbon-emission/product-overview",
            "https://docs.jdcloud.com/cn/iot-park/product-overview",
            "https://docs.jdcloud.com/cn/iot-estate/product-overview",
            "https://docs.jdcloud.com/cn/iot-community/product-overview",
            "https://docs.jdcloud.com/cn/iot-smartdev/product-overview",
            "https://docs.jdcloud.com/cn/iot-bulkstock/product-overview",
            "https://docs.jdcloud.com/cn/moiot/productoverview",
            "https://docs.jdcloud.com/cn/iov-mobility-service/product-overview",
            "https://docs.jdcloud.com/cn/jdwhale-dcs/product-overview",
            "https://docs.jdcloud.com/cn/EcoBuildOps/product-overview",
            "https://docs.jdcloud.com/cn/coc-virtual-machines/product-overview",
            "https://docs.jdcloud.com/cn/coc-disk/product-overview",
            "https://docs.jdcloud.com/cn/coc-virtual-private-cloud/product-overview",
            "https://docs.jdcloud.com/cn/coc-elastic-ip/product-overview",
            "https://docs.jdcloud.com/cn/virtual-machines-x/product-overview",
            "https://docs.jdcloud.com/cn/nlp-textfluencyrecognition/nlp-textfluencyrecognition",
            "https://docs.jdcloud.com/cn/orc-translationrecognition/orc-translationrecognition",
            "https://docs.jdcloud.com/cn/iot-device-sdk/introduction",
            "https://docs.jdcloud.com/cn/jdcloud-security-whitepaper/introduction",
            "https://docs.jdcloud.com/cn/resourcegroup/productintroduction",
            "https://docs.jdcloud.com/cn/security-instruction/intel-meltdown-spectre-solution",
            "https://docs.jdcloud.com/cn/learn-best-practice/construction-of-jdcloud-high-availability-architecture",
            "https://docs.jdcloud.com/cn/account-assets/fund-flow",
            "https://docs.jdcloud.com/cn/online-buying/transaction-details",
            "https://docs.jdcloud.com/cn/payment/payment-methods",
            "https://docs.jdcloud.com/cn/invoice/invoice-application-process",
            "https://docs.jdcloud.com/cn/billing/prepay",
            "https://docs.jdcloud.com/cn/contract-management/contract-application-process",
            "https://docs.jdcloud.com/cn/billingcost/overview",
            "https://docs.jdcloud.com/cn/expense-budget/overview",
            "https://docs.jdcloud.com/cn/resourceconsumption/overview",
            "https://docs.jdcloud.com/cn/account-management/sign-in-and-sign-up",
            "https://docs.jdcloud.com/cn/real-name-verification/introduction",
            "https://docs.jdcloud.com/cn/message-center/message-management",
            "https://docs.jdcloud.com/cn/security-operation-protection/product-overview",
            "https://docs.jdcloud.com/cn/jdcloudapp/introduction",
            "https://docs.jdcloud.com/cn/marketplace/marketplace-introduction",
            "https://docs.jdcloud.com/cn/platform-agreement/registration-agreement",
            "https://docs.jdcloud.com/cn/copyright/copyright",
            "https://docs.jdcloud.com/cn/service-content/service-content",
            "https://docs.jdcloud.com/cn/contact-us/contact-us"
        ]

        # urls=["https://docs.jdcloud.com/cn/jcs-for-kubernetes/product-overview"]

        # filename = f"{self.root_dir}incorrect_docs.csv"
        filename = incorrect_filename
        if os.path.exists(filename):
            os.remove(filename)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'filename': filename})

    def parse(self, response):
        # dir_path = self.root_dir+response.url.split("/")[-2]
        # isExists = os.path.exists(dir_path)
        # if isExists:
        #     os.rmdir(dir_path)
        # os.makedirs(dir_path)
        filename = response.meta["filename"]
        time.sleep(1)
        url_list = response.selector.xpath(
            '//ul[contains(@class,"nav-inner-list")]/li/a/@href').getall()
        for url in url_list:
            print(url)
            if url == "javascript:;":
                continue
            url = "https://docs.jdcloud.com"+url
            # yield scrapy.Request(url=url, callback=self.check_docs, meta={'dir_path': dir_path})
            yield scrapy.Request(url=url, callback=self.check_docs, meta={'filename': filename})

    def check_docs(self, response):
        # dir = response.meta["dir_path"]
        # name = response.url.split("/")[-1]
        url = response.url

        # filename = f"{dir}/{name}.json"
        # filename = f"{self.root_dir}/incorrect_docs.json"
        filename = response.meta["filename"]

        incorrect_docs_record_file = open(filename, "a+")

        title = response.selector.xpath("//title/text()").get()
        title_list = title.split("--")
        # 文档title
        doc_title = title_list[0]
        # 产品名称
        prd = title_list[1].split('-')[0]

        js = response.selector.xpath("//body/script/text()").get()
        # 解析script 中的函数
        fun = re.search(
            r"window\.__NUXT__=\(function\((.*?)\)\s*{([\s\S]*?)}\((.*?)\)\);", js, re.M).group(2)
        # 提取aP.content 的 markdown内容
        content = re.search(r".content\s*=\s*\"(.*)\";",
                            fun, re.M).group(1).replace("\\n", "\n")

        checked = check_content(content=content, url=url)

        if checked != None:
            line = str(checked.incorrect_reason)+"," + \
                str(prd)+","+checked.url
            incorrect_docs_record_file.write(line+"\n")
            # incorrect_docs_record_file.write(checked.model_dump_json()+"\n")
            incorrect_docs_record_file.close()
            self.log(f"append {filename}:{checked.model_dump_json()}")


def is_html(content):
    if content.startswith('<'):
        return True
    else:
        return False


def replace_unicode(match):
    """
    usecase:
    替换Unicode字符为str
    result = re.sub(r"\\[uU]([0-9a-fA-F]{4})", replace_unicode, lines)
    """
    code_point = int(match.group(1), 16)
    return chr(code_point)


def include_unicode(text):
    match = r"\\[uU]([0-9a-fA-F]{4})"
    if re.search(r"\\[uU]([0-9a-fA-F]{4})", text):
        return True
    else:
        return False


def start_with_unicode(text):
    match = r"^\\[uU]([0-9a-fA-F]{4})"
    if re.search(match, text):
        return True
    else:
        return False


def check_content(content, url):
    if start_with_unicode(content):
        return bad_doc_json(url=url, incorrect_reason=Reason.StartWithUnicode)

    result = re.sub(r"\\[uU]([0-9a-fA-F]{4})", replace_unicode, content)

    if is_html(result):
        return bad_doc_json(url=url, incorrect_reason=Reason.IsHtml)

    return None

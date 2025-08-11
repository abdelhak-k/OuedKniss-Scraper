from settings import COUNT

def get_payload_search(category_slug, page):
    """
    # you can filter the posts you're interested in
    # categorySlug will filter what type of product you're interested in
    # how can I get the categorySlug name? you should do it manually; go to www.ouedkniss.com with the developer mode and see what requests has been sent
    # you will find some examples in the main
    # and select graphql the one one with operation name: SearchQuery
    # count is the number of posts you will in a single query
    # you can still get other informations, check the payload on the request sent from www.ouedkniss.com
    """
    return {
        "operationName": "SearchQuery",
        "variables": {
            "q": None,
            "filter": {
                "categorySlug": category_slug,
                "origin": None,
                "connected": False,
                "delivery": None,
                "regionIds": [],
                "cityIds": [],
                "priceRange": [None, None],
                "exchange": None,
                "hasPictures": False,
                "hasPrice": False,
                "priceUnit": None,
                "fields": [],
                "page": page,
                "orderByField": {"field": "REFRESHED_AT"},
                "count": COUNT
            }
        },
        "query": """
        query SearchQuery($q: String, $filter: SearchFilterInput) {
            search(q: $q, filter: $filter) {
                announcements {
                    data {
                        id
                    }
                    paginatorInfo {
                        lastPage
                        hasMorePages
                    }
                }
            }
        }
        """
    }

def get_payload_post_all(ann_id):
    # all available data from the API
    # NOTE: YOU can remove the unwanted features to make the process much faster
    return {
        "operationName": "AnnouncementGet",
        "variables": {"id": str(ann_id)},
        "query": """
        query AnnouncementGet($id: ID!) {
            announcement: announcementDetails(id: $id) {
                id
                reference
                title
                slug
                description
                orderExternalUrl
                createdAt: refreshedAt
                price
                pricePreview
                oldPrice
                oldPricePreview
                priceType
                exchangeType
                priceUnit
                hasDelivery
                deliveryType
                hasPhone
                hasEmail
                quantity
                status
                street_name
                category {
                    id
                    slug
                    name
                    deliveryType
                    parentTree {
                        id
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                defaultMedia(size: ORIGINAL) {
                    mediaUrl
                    mimeType
                    thumbnail
                    __typename
                }
                medias(size: LARGE) {
                    mediaUrl
                    mimeType
                    thumbnail
                    __typename
                }
                categories {
                    id
                    name
                    slug
                    parentId
                    __typename
                }
                specs {
                    specification {
                        label
                        codename
                        type
                        __typename
                    }
                    value
                    valueText
                    __typename
                }
                user {
                    id
                    username
                    displayName
                    avatarUrl
                    __typename
                }
                isFromStore
                store {
                    id
                    name
                    slug
                    description
                    imageUrl
                    url
                    followerCount
                    viewAsStore
                    announcementsCount
                    status
                    locations {
                        location {
                            address
                            region {
                                slug
                                name
                                __typename
                            }
                            __typename
                        }
                        __typename
                    }
                    categories {
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                cities {
                    id
                    name
                    region {
                        id
                        name
                        slug
                        __typename
                    }
                    __typename
                }
                isCommentEnabled
                noAdsense
                variants {
                    id
                    hash
                    specifications {
                        specification {
                            codename
                            label
                            __typename
                        }
                        valueText
                        value
                        mediaUrl
                        __typename
                    }
                    price
                    oldPrice
                    pricePreview
                    oldPricePreview
                    quantity
                    __typename
                }
                showAnalytics
                messengerLink
                __typename
            }
        }
        """
    }

def get_payload_post_mini(ann_id):
    return {
        "operationName": "AnnouncementGet",
        "variables": {"id": str(ann_id)},
        "query": """
        query AnnouncementGet($id: ID!) {
            announcement: announcementDetails(id: $id) {
                reference
                title
                description
                pricePreview
                priceUnit
                createdAt: refreshedAt
                specs {
                    specification {
                        label
                    }
                    valueText
                }
                cities {
                    name
                }
            }
        }
        """
    }
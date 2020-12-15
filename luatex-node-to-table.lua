json = require "json"
inspect = require "inspect"

-- load JSON object from file
function read_luatex_node_json()
    local filename = "luatex-node.json"
    local file = io.open(filename, "r")
    local str = file:read("a")
    file:close()
    local json_obj = json.decode(str)
    return json_obj
end

json_obj = read_luatex_node_json()

-- get the corresponding JSON entry for a node
function get_json_entry(n)
    local node_type = json_obj["_node_id"][tostring(n.id)]

    if node_type == nil then
        return nil
    end

    if node_type == "whatsit" then
        local whatsit_subtype = json_obj["_whatsit_id"][tostring(n.subtype)]
        local key = "whatsit_" .. whatsit_subtype
        local ret = json_obj[key]
        if ret ~= nil then
            ret["subtype"] = json_obj["_whatsit_id"]
        end
        return ret
    else
        return json_obj[node_type]
    end

end

-- get an attribute from node
function node_get(n, ind)
    local indexer = getmetatable(n).__index
    return indexer(n, ind)
end

function generic_describe_text_format(a, b)
    a = tostring(a)
    b = tostring(b)
    return string.format("%s(%s)", a, b)
end

function generic_describe_text(n, json_entry, key)
    local val = node_get(n, key)
    local des = json_entry[key][tostring(val)]
    des = des or "*unknown*"
    return generic_describe_text_format(des, val)
end

function has_key(tbl, key)
    local test = tbl[key]
    return test ~= nil
end

function shallowcopy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == "table" then
        copy = {}
        for orig_key, orig_value in pairs(orig) do
            copy[orig_key] = orig_value
        end
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
end

function get_default_param()
    local ret = {}
    ret["expand_depth"] = 2
    ret["convert_dim_to_pt"] = true
    ret["expand_next"] = false
    ret["expand_prev"] = false
    ret["show_char"] = true
    return ret
end

function handle_id(n, param)
    return generic_describe_text_format(node.type(n.id), n.id)
end

function handle_dim(n, param)
    local target = node_get(n, param["current_key"])
    if param["convert_dim_to_pt"] then
        return string.format("%fpt", target / 65536)
    end
    return target
end

function handle_other_node(n, param)
    local target = node_get(n, param["current_key"])
    if param["expand_depth"] <= 0 then
        if target == nil then
            return {}
        else
            return {tostring(target)}
        end
    end
    local new_param = shallowcopy(param)
    new_param["expand_depth"] = new_param["expand_depth"] - 1
    return luatex_node_to_table(target, new_param)
end

function handle_prev(n, param)
    if param["expand_prev"] then
        return handle_other_node(n, param)
    end
    dummy_param = shallowcopy(param)
    dummy_param["expand_depth"] = 0
    return handle_other_node(n, dummy_param)
end

function handle_next(n, param)
    if param["expand_next"] then
        return handle_other_node(n, param)
    end
    dummy_param = shallowcopy(param)
    dummy_param["expand_depth"] = 0
    return handle_other_node(n, dummy_param)
end

function handle_char(n, param)
    if param["show_char"] then
        return string.format("'%s'(%d)", string.char(n.char), n.char)
    end
    return n.char
end

function attribute_list_node_to_table(n, param)
    local ret = {}
    ret["id"] = generic_describe_text_format("attribute_list", node.id("attribute_list"))
    for attr_n in node.traverse(n.next) do
        local key = tostring(attr_n.number)
        ret[key] = attr_n.value
    end
    return ret
end

function handle_attr(n, param)
    return attribute_list_node_to_table(n.attr, param)
end

-- field handlers
field_special_handler = {
    id = handle_id,
    width = handle_dim,
    height = handle_dim,
    depth = handle_dim,
    prev = handle_prev,
    next = handle_next,
    char = handle_char,
    attr = handle_attr
}


function luatex_node_to_table(n, param)
    param = param or get_default_param()

    local json_entry = get_json_entry(n)

    local ret = {}

    if json_entry ~= nil then
        local field = json_entry["_field"]
        assert(field ~= nil, "invalid entry")
        for _, key in pairs(field) do
            local field_val = node_get(n, key) or {}
            param["current_key"] = key
            -- see if there is special handler
            if has_key(field_special_handler, key) then
                local handler = field_special_handler[key]
                ret[key] = handler(n, param)
            elseif has_key(json_entry, key) then
                -- see if the key is in `json_entry`, which means we can use generic handler
                ret[key] = generic_describe_text(n, json_entry, key)
            elseif node.is_node(field_val) then
                -- special treatment when the attribute is a node
                ret[key] = handle_other_node(n, param)
            else
                ret[key] = field_val
            end
        end
    else
        texio.write_nl(string.format("unseen node type %s", node.type(n.id)))
        table.insert(ret, tostring(n))
    end

    return ret
end

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from slither import Slither
import os
from slither.detectors.all_detectors import *
from slither.printers.all_printers import *

detectors_to_register = [Backdoor, UninitializedStateVarsDetection, UninitializedStorageVars, UninitializedLocalVars, VarReadUsingThis, ConstantPragma, IncorrectSolc, LockedEther, ArbitrarySendEth, ArbitrarySendErc20NoPermit, ArbitrarySendErc20Permit, Suicidal, ReentrancyBenign, ReentrancyReadBeforeWritten, ReentrancyNoGas, ReentrancyEth, ReentrancyEvent, UnusedStateVars, CouldBeConstant, CouldBeImmutable, TxOrigin, Assembly, LowLevelCalls, UnusedReturnValues, UncheckedTransfer, NamingConvention, ExternalFunction, ControlledDelegateCall, ConstantFunctionsAsm, ConstantFunctionsState, ShadowingAbstractDetection, StateShadowing, LocalShadowing, BuiltinSymbolShadowing, Timestamp, MultipleCallsInLoop, IncorrectStrictEquality, IncorrectERC20InterfaceDetection, IncorrectERC721InterfaceDetection, UnindexedERC20EventParameters, DeprecatedStandards, RightToLeftOverride, TooManyDigits, UncheckedLowLevel, UncheckedSend, VoidConstructor, TypeBasedTautology, BooleanEquality, BooleanConstantMisuse, DivideBeforeMultiply, UnprotectedUpgradeable, NameReused, UnimplementedFunctionDetection, MappingDeletionDetection, ArrayLengthAssignment, SimilarVarsDetection, FunctionInitializedState, RedundantStatements, BadPRNG, CostlyOperationsInLoop, AssertStateChange, MissingInheritance, ShiftParameterMixup, StorageSignedIntegerArray, UninitializedFunctionPtrsConstructor, ABIEncoderV2Array, ArrayByReference, EnumConversion, MultipleConstructorSchemes, PublicMappingNested, ReusedBaseConstructor, MissingEventsAccessControl, MissingEventsArithmetic, ModifierDefaultDetection, PredeclarationUsageLocal, IncorrectUnaryExpressionDetection, MissingZeroAddressValidation, DeadCode, WriteAfterWrite, MsgValueInLoop, DelegatecallInLoop,ProtectedVariables, DomainSeparatorCollision, Codex]
printers_to_register = [FunctionSummary, ContractSummary]


app = Flask(__name__)
@app.route('/')
def home():
    return 'Welcome to my API!'

@app.route('/api/data')
def get_data():
    data = {'name': 'John', 'age': 30, 'city': 'New York'}
    return data

@app.route('/analyze', methods=['POST'])
def analyze_contract():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    solidity_file = request.files['file']
    if not solidity_file.filename.endswith('.sol'):
        return jsonify({'error': 'Invalid file type'}), 400

    # Crea la carpeta si no existe
    dir_path = 'contracts'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    # Guarda el archivo
    file_path = os.path.join('contracts', secure_filename(solidity_file.filename))
    try:
        solidity_file.save(file_path)
    except:
        return jsonify({'error': 'Error saving file'}), 400

    # Verifica si el archivo se guardó correctamente
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Error saving file'}), 400

    # Registra los detectores
    slither = Slither(file_path)
    for detector in detectors_to_register:
        slither.register_detector(detector)

    # Ejecuta los detectores y retorna los resultados
    try:
        results = slither.run_detectors()
    except:
        return jsonify({'error': 'Error running detectors'}),  400

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)